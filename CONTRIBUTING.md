# Contributing to VetHub

VetHub welcomes additions and corrections to the veterinary open-resource registry.

## Fastest way to suggest a resource

Open the **Submit a veterinary resource** issue template and provide the canonical URL.

## Pull-request submissions

For reviewed resources, add an entry to:

```text
registry/repositories.yaml
```

For uncertain or machine-discovered resources, use:

```text
registry/candidates.yaml
```

Do not copy third-party source code, datasets, or model weights into VetHub. Link to the canonical upstream resource.

## Inclusion principles

A resource should have a meaningful connection to veterinary medicine, animal health, animal welfare, veterinary public health, veterinary research, or a clearly veterinary-facing One Health use case.

Generic animal examples, toy dog/cat classifiers, and unrelated machine-learning demos should not be accepted solely because they contain animal terminology.

## Metadata corrections

Dynamic GitHub metadata is refreshed automatically. Human-curated taxonomy fields may be corrected through pull requests.

## Local validation

```bash
pip install -e ".[dev]"
vethub validate
pytest
```
