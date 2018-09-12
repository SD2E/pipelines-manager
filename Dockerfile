FROM sd2e/reactors:python3

# reactor.py, config.yml, and message.jsonschema will be automatically
# added to the container when you run docker build or abaco deploy
COPY datacatalog /datacatalog

COPY message.jsonschema /schemas/create.jsonschema
COPY manage.jsonschema /schemas/manage.jsonschema
COPY delete.jsonschema /schemas/delete.jsonschema
