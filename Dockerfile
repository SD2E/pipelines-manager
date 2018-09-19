FROM sd2e/reactors:python3-edge

COPY message.jsonschema /schemas/create.jsonschema
COPY manage.jsonschema /schemas/manage.jsonschema
COPY delete.jsonschema /schemas/delete.jsonschema
