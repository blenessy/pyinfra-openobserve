# pyinfra-openobserve

This pyinfra deploy package provides two simple deploy targets for OpenObserve:

- `deploy_openobserve_agent`: Installs the OpenObserve Agent on a target host
- `deploy_openobserve_server`: Installs the OpenObserve Server on a target host

## Inventory Defaults

Check [src/pyinfra_openobserve/defaults.py](src/pyinfra_openobserve/defaults.py) for the
defaults values. You can override these in the inventory file.

### Overriding Templates

You can override a default template by putting a modified version of it in your 
custom template path.

The `primary_templates_path` argument tells deploy functions to prioritize your
modified templates (if those exist), falling back to the default template if does not.

## deploy_openobserve_agent

### Arguments

| Key | Default | Description |
| --- | --- | --- |
| `otel_url` | | OpenObserve OTEL endpoint URL |
| `username` | | OpenObserve username |
| `password` | | OpenObserve password |
| `primary_templates_path` | None | Load templates from this path before falling back to the default templates path |

## deploy_openobserve_server

### Arguments

| Key | Default | Description |
| --- | --- | --- |
| `root_user_email` | | OpenObserve root user email |
| `root_user_password` | | OpenObserve root user password |
| `primary_templates_path` | None | Load templates from this path before falling back to the default templates path |

### Edition

The server defaults to the Open Source (`o2`) edition. Set `o2_server_edition: "o2-enterprise"` in your inventory to install the Enterprise build instead.

### Security notes

The rendered `openobserve.env` (containing the root user password) is written with mode `0640` and owned by the `openobserve-server` user and group. Never commit real `root_user_password` values in inventory files.


## NOTICE

Inspired by: https://github.com/grantstephens/pyinfra-prometheus
