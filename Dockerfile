FROM sd2e/reactors:python3-edge

# Comment out if not actively developing python-datacatalog
ARG DATACATALOG_BRANCH=0_2_0
RUN pip uninstall --yes datacatalog || true
RUN pip3 install --upgrade --no-cache-dir \
    git+https://github.com/SD2E/python-datacatalog.git@${DATACATALOG_BRANCH}

COPY schemas /schemas
