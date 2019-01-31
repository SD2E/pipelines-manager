=================
Pipelines Manager
=================

This Reactor enables creation and management of Data Catalog **Pipelines**.

Messages
--------

All Pipeline management actions are accomplished by sending JSON-formatted
messages. These are documented in detail below in JSONSchemas_.

Create a New Pipeline
---------------------

.. code-block:: console

    $ abaco run -m "$(jq -c . my_pipeline.json)" G1p783PxpalBB

    gOvQRGRVPPOzZ

    # Wait a few seconds

    $ abaco logs G1p783PxpalBB gOvQRGRVPPOzZ

    EGe6NKeo8Oy5 DEBUG Action selected: create
    EGe6NKeo8Oy5 INFO Created pipeline 1064aaf1-459c-5e42-820d-b822aa4b3990 with update token 0df45d5e9e0f31e2

Take note of the pipeline's UUID (i.e. ``1064aaf1-459c-5e42-820d-b822aa4b3990``)
as it is needed to configure code and scripts that launch jobs.

Update a Pipeline
-----------------

A pipeline's *components* cannot be updated, but its human-readable name and
description can be. This is by design, as the components define a distinct set
of assets and shared parameters for accomplishing a specific task.

*Coming soon...*

Retire a Pipeline
-----------------

A pipeline cannot be deleted, but it can be retired from active service.

*Coming soon...*

.. _JSONSchemas:

JSON Schemas
------------

.. literalinclude:: schemas/create.jsonschema
   :language: json
   :linenos:
   :caption: pipeline_manager_create

.. literalinclude:: schemas/update.jsonschema
   :language: json
   :linenos:
   :caption: pipeline_manager_update

.. literalinclude:: schemas/deletejsonschema
   :language: json
   :linenos:
   :caption: pipeline_manager_delete
