FROM sd2e/reactors:python3

# reactor.py, config.yml, and message.jsonschema will be automatically
# added to the container when you run docker build or abaco deploy
COPY datacatalog /datacatalog

COPY create.jsonschema /schemas/create.jsonschema
COPY update.jsonschema /schemas/update.jsonschema
COPY delete.jsonschema /schemas/delete.jsonschema
