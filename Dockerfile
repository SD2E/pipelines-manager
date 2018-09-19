FROM sd2e/reactors:python3-edge

COPY create.jsonschema /schemas/create.jsonschema
COPY update.jsonschema /schemas/update.jsonschema
COPY delete.jsonschema /schemas/delete.jsonschema
