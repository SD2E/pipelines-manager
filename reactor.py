import os
import json
from attrdict import AttrDict
from pprint import pprint
from reactors.runtime import Reactor, agaveutils
from datacatalog.pipelines import PipelineStore, PipelineCreateFailure, PipelineUpdateFailure
from datacatalog.identifiers import datacatalog_uuid

def main():

    r = Reactor()
    m = AttrDict(r.context.message_dict)
    if m == {}:
        try:
            print(r.context.raw_message)
            jsonmsg = json.loads(r.context.raw_message)
            m = jsonmsg
        except Exception:
            pass

    try:
        r.validate_message(m, permissive=False)
    except Exception as exc:
        r.on_failure('Failed to validate message', exc)

    if '__options' in m:
        # allow override of settings
        try:
            options_settings = m.get('__options', {}).get('settings', {})
            if isinstance(options_settings, dict):
                options_settings = AttrDict(options_settings)
            r.settings = r.settings + options_settings
        except Exception as exc:
            r.on_failure('Failed to handle options', exc)

    # small-eel/w7M4JZZJeGXml/EGy13KRPQMeWV
    stores_session = '/'.join([r.nickname, r.uid, r.execid])

    # Set up Store objects
    pipe_store = PipelineStore(mongodb=r.settings.mongodb,
                               config=r.settings.catalogstore,
                               session=stores_session)

    create_dict = {}
    for k in pipe_store.CREATE_OPTIONAL_KEYS:
        if k in m:
            create_dict[k] = m.get(k)

    try:
        new_pipeline = pipe_store.create(m.get('components', []), **create_dict)
        r.logger.info('Successfully created pipeline {}'.format(str(new_pipeline['uuid'])))
    except Exception as exc:
        r.on_failure('Create failed', exc)

if __name__ == '__main__':
    main()
