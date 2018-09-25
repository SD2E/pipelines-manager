import os
import json
import copy

from attrdict import AttrDict
from pprint import pprint
from jsonschema import ValidationError

from reactors.runtime import Reactor, agaveutils
from datacatalog.pipelines import PipelineStore, PipelineCreateFailure, PipelineUpdateFailure

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
        for a in ['create', 'update', 'delete', 'undelete']:
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
            m.pop('__options')
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
        create_dict = copy.deepcopy(m)
        try:
            new_pipeline = pipe_store.create(**create_dict)
            r.on_success('Created pipeline {} with update token {}'.format(
                new_pipeline['_uuid'], new_pipeline['token']))
        except Exception as exc:
            r.on_failure('Create failed', exc)

    if action == 'update':
        update_dict = m.get('body', {})
        try:
            new_pipeline = pipe_store.update_pipeline(
                pipeline_uuid=m['uuid'], update_token=m['token'], **update_dict)
            r.on_success('Updated pipeline {}'.format(
                new_pipeline['_uuid']))
        except Exception as exc:
            r.on_failure('Update failed', exc)

    if action == 'delete':
        try:
            pipe_store.delete(m['uuid'], m['token'], m.get('force', False))
            r.on_success('Deleted pipeline {}'.format(m.get('uuid')))
        except Exception as exc:
            r.on_failure('Delete failed', exc)

    if action == 'undelete':
        try:
            pipe_store.undelete(m['uuid'], m['token'])
            r.on_success('Un-deleted pipeline {}'.format(m.get('uuid')))
        except Exception as exc:
            r.on_failure('Undelete failed', exc)


if __name__ == '__main__':
    main()
