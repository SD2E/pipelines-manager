=================
Pipelines Manager
=================

This Reactor enables creation and management of Data Catalog **Pipelines**.


Create a New Pipeline
---------------------

.. code-block:: console

    $ abaco run -F 0-tacobot.json -x kOYmxWRq5X4K7
    kOYmxWRq5X4K7 DEBUG Action selected: create
    kOYmxWRq5X4K7 INFO Creating pipeline...
    kOYmxWRq5X4K7 INFO Wrote pipeline 10675c08-f803-5ccb-b508-e56f49888dca; Update token: 365bc32258cf546a

Take note of the pipeline's UUID (i.e. ``1064aaf1-459c-5e42-820d-b822aa4b3990``)
as it is needed to configure code and scripts that launch jobs. Note also the
pipeline's update token (``365bc32258cf546a``) as it is required to manage the
pipeline at a future time. An admin token may be provided in place of the
document-specific token if you are able to generate one.

Update a Pipeline
-----------------

A pipeline's *components* cannot be updated, but other attributes can. This is
by design, as components define a distinct set of assets and shared parameters
for accomplishing a specific task and are thus the basis for reproducible
computation.

Assuming the edited JSON doc is called ``1-tacobot.json``, pass along the new
document contents along with its UUID and the update token like so:

.. code-block:: console

    $  abaco run -F 1-tacobot.json -q 'uuid=10675c08-f803-5ccb-b508-e56f49888dca&token=365bc32258cf546a' -x kOYmxWRq5X4K7
    kOYmxWRq5X4K7 DEBUG Action selected: create
    kOYmxWRq5X4K7 INFO Replacing 10675c08-f803-5ccb-b508-e56f49888dca
    kOYmxWRq5X4K7 INFO Wrote pipeline 10675c08-f803-5ccb-b508-e56f49888dca; Update token: 0898ac57b681c3df


Disable a Pipeline
-----------------

A pipeline cannot be deleted, but it can be retired from active service. One
passes an empty message ``{}``, the UUID and token, as well as the action
name "disable". Note that unlike after an "update" action, the token does
not change and is thus not reported.

.. code-block:: console

    $ abaco run -m {} -q 'uuid=10675c08-f803-5ccb-b508-e56f49888dca&token=0898ac57b681c3df&action=disable' -x kOYmxWRq5X4K7
    kOYmxWRq5X4K7 DEBUG Action selected: disable
    kOYmxWRq5X4K7 INFO Disabling pipeline 10675c08-f803-5ccb-b508-e56f49888dca
    kOYmxWRq5X4K7 INFO Success

Restore a Pipeline
------------------

To restore an disabled pipeline, pass an empty message ``{}``, the pipeline
UUID and access token, and action name "enable". Note that unlike after an
"update" action, the token does not change and is thus not reported.


.. code-block:: console

    $ abaco run -m {} -q 'uuid=10675c08-f803-5ccb-b508-e56f49888dca&token=0898ac57b681c3df&action=enable' -x kOYmxWRq5X4K7
    kOYmxWRq5X4K7 DEBUG Action selected: enable
    kOYmxWRq5X4K7 INFO Enabling pipeline 10675c08-f803-5ccb-b508-e56f49888dca
    kOYmxWRq5X4K7 INFO Success

