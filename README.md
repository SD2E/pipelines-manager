# Pipelines Manager

Implements a Reactor that provides create/update/delete functionality for Data
Catalog Pipeline entities. To use, send a message following one of the three
JSON schemas to either the production or staging actorId. The production actor
writes to the main `catalog` database while staging writes to `catalog_staging`

## Example Workflow

```shell

$ abaco run -m '`cat my_pipeline.json`' G1p783PxpalBB

