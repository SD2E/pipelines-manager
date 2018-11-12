FROM sd2e/reactors:python3-edge

# Comment out if not actively developing python-datacatalog
RUN pip uninstall --yes datacatalog || true
# COPY datacatalog /datacatalog

# Install from Repo
RUN pip3 install --upgrade git+https://github.com/SD2E/python-datacatalog.git@develop

COPY create.jsonschema /schemas/create.jsonschema
COPY update.jsonschema /schemas/update.jsonschema
COPY delete.jsonschema /schemas/delete.jsonschema
COPY undelete.jsonschema /schemas/undelete.jsonschema
