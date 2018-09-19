import os
import json
from attrdict import AttrDict
from pprint import pprint
from reactors.runtime import Reactor, agaveutils
from jsonschema import ValidationError
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

    action = None
    try:
        for a in ['create', 'update', 'delete']:
            try:
                schema_file = '/schemas/' + a + '.jsonschema'
                r.validate_message(
                    m, messageschema=schema_file, permissive=False)
                action = a
                break
            except Exception as exc:
                r.logger.debug('Validation to "{0}" failed: {1}\n'.format(a, exc))
        if action is None:
            raise ValidationError('Message did not match any known schema')
    except Exception as vexc:
        r.on_failure('Failed to process message', vexc)

    r.logger.debug('Action selected: {}'.format(action))

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
                               config=r.settings.get('catalogstore', {}),
                               session=stores_session)

    if action == 'create':
        create_dict = {}
        for k in pipe_store.CREATE_OPTIONAL_KEYS:
            if k in m:
                create_dict[k] = m.get(k)

        try:
            new_pipeline = pipe_store.create(m.get('components', []), **create_dict)
            r.on_success('Created pipeline {} with update token {}'.format(
                new_pipeline['_uuid'], new_pipeline['token']))
        except Exception as exc:
            r.on_failure('Create failed', exc)

    # FIXME Implement 'update' here and in datacatalog.pipelines.store

    if action == 'delete':
        # FIXME Implement soft delete based on _visible key
        try:
            pipe_store.delete(uuid=m.get('uuid'), token=m.get('token'), force=True)
            r.on_success('Successfully deleted pipeline {}'.format(m.get('uuid')))
        except Exception as exc:
            r.on_failure('Delete failed', exc)

if __name__ == '__main__':
    main()
