import os
import json
import copy

from attrdict import AttrDict
from pprint import pprint
from jsonschema import ValidationError
from reactors.runtime import Reactor, agaveutils

from datacatalog.linkedstores.basestore import strategies
from datacatalog.linkedstores.pipeline import (PipelineStore,
                                               PipelineCreateFailure,
                                               PipelineUpdateFailure)


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

    # Allow passed vars to override
    token = os.environ.get('token', None)
    uuid = os.environ.get('uuid', None)
    if uuid:
        action = os.environ.get('action', 'show')
    else:
        action = None

    try:
        for a in ['create']:
            try:
                schema_file = '/schemas/' + a + '.jsonschema'
                r.validate_message(m,
                                   messageschema=schema_file,
                                   permissive=False)
                action = a
                break
            except Exception as exc:
                if action not in ('enable', 'disable'):
                    r.logger.debug('Validation to "{0}" failed: {1}\n'.format(
                        a, exc))
        if action is None:
            raise ValidationError('Message did not match any known schema')
    except Exception as vexc:
        r.on_failure('Failed to process message', vexc)

    r.logger.debug('Action selected: {}'.format(action))

    # Set up Store objects
    pipe_store = PipelineStore(mongodb=r.settings.mongodb)

    if action == 'get':
        resp = pipe_store.find_one_by_uuid(uuid)
        r.logger.info(resp)
        r.on_success('Exists and was printed to execution log')

    if action == 'create':
        create_dict = copy.deepcopy(m)
        try:
            if uuid and token:
                r.logger.info('Replacing {}'.format(uuid))
                pipeline = pipe_store.add_update_document(
                    create_dict,
                    uuid=uuid,
                    token=token,
                    strategy=strategies.REPLACE)
            else:
                r.logger.info('Creating pipeline...')
                pipeline = pipe_store.add_update_document(create_dict)
            r.on_success('Wrote pipeline {}; Update token: {}'.format(
                pipeline['uuid'], pipeline['_update_token']))
        except Exception as exc:
            r.on_failure('Write failed', exc)

    if action == 'disable':
        try:
            r.logger.info('Disabling pipeline {}'.format(uuid))
            resp = pipe_store.delete_document(uuid, token, force=False)
            r.on_success('Success')
        except Exception as exc:
            r.on_failure('Disable failed', exc)

    if action == 'enable':
        try:
            r.logger.info('Enabling pipeline {}'.format(uuid))
            resp = pipe_store.undelete(uuid, token)
            r.on_success('Success')
        except Exception as exc:
            r.on_failure('Enable failed', exc)


if __name__ == '__main__':
    main()
