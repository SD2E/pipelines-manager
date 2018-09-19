# Pipelines Manager

Implements a Reactor that provides create/update/delete functionality for Data
Catalog Pipeline entities. To use, send a message following one of the three
JSON schemas to either the production or staging actorId. The production actor
writes to the main `catalog` database while staging writes to `catalog_staging`

## Usage

### Create a new pipeline

```shell

$ abaco run -m "$(jq -c . my_pipeline.json)" G1p783PxpalBB

gOvQRGRVPPOzZ

# Wait a few seconds

$ abaco logs G1p783PxpalBB gOvQRGRVPPOzZ

EGe6NKeo8Oy5 DEBUG Action selected: create
EGe6NKeo8Oy5 INFO Created pipeline eb8deee6-1c72-5331-bfe6-37afa63665fe with update token 0df45d5e9e0f31e2
```

### Update the pipelin's name or description

You can't update the components (this is by design) but you can update its human-readable name and description.

(TBD)

### Delete the pipeline

```shell

$ abaco run -m '{"uuid": "eb8deee6-1c72-5331-bfe6-37afa63665fe", "action": "delete", "token": "0df45d5e9e0f31e2"}' G1p783PxpalBB

```
