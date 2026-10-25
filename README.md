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

This installs a single-node OpenObserve Server from the official release binaries at
`downloads.openobserve.ai`, verifies the tarball's SHA256, and runs it as the `openobserve`
systemd service listening on `o2_server_bind_addr:o2_server_http_port` (default `0.0.0.0:5080`)
with data stored in `o2_server_data_dir`.

The root user credentials are only used by OpenObserve on first startup; changing them
afterwards does not change the existing root user's password.

### Edition

The server defaults to the Open Source (`opensource`) edition. Set `o2_server_edition: "enterprise"`
in your inventory to install the Enterprise build instead.

SHA256 sums for each edition, OS and architecture are listed in `o2_server_sha256sums`. If you
override `o2_server_version`, also override `o2_server_sha256sums` with the values from the
official `<tarball>.sha256sum` files, otherwise the checksum verification is skipped.

### Security notes

The rendered `openobserve.env` (containing the root user password) is written with mode `0640` and owned by the `openobserve-server` user and group. Never commit real `root_user_password` values in inventory files.


## NOTICE

Inspired by: https://github.com/grantstephens/pyinfra-prometheus
