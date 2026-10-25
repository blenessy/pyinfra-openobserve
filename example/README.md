# pyinfra-openobserve Example

Example usage of pyinfra-openobserve to deploy the OpenObserve OTEL agent and (optionally) a single-node OpenObserve Server on a remote host.

## Running the example locally

Create `inventory.py` (it is gitignored, never commit it). Pick one of the shapes below.

### Agent only, shipping to OpenObserve Cloud

```python
my_servers = [
    (
        "myhost",
        {
            "ssh_hostname": "1.2.3.4",
            "ssh_user": "root",
            "o2_otel_url": "https://eu1-api.openobserve.ai/api/xxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "o2_username": "john@example.com",
            "o2_password": "o2oi_**********************",
        },
    )
]
```

### Self-hosted server, with the agent shipping to it

```python
my_servers = [
    (
        "myhost",
        {
            "ssh_hostname": "1.2.3.4",
            "ssh_user": "root",
            # OpenObserve Server (the root user is only created on first startup)
            "o2_server_root_user_email": "root@example.com",
            "o2_server_root_user_password": "**********************",
            # OpenObserve Agent, shipping to the server's "default" organization
            "o2_otel_url": "http://localhost:5080/api/default",
            "o2_username": "root@example.com",
            "o2_password": "**********************",
        },
    )
]
```

The server deploy is opt-in: `deploy.py` only installs the OpenObserve Server when `o2_server_root_user_email` is set for the host. It runs before the agent deploy so the agent can ship to a server on the same host.

The example installs the Open Source edition. Change `o2_server_edition` to `"enterprise"` in `group_data/all.py` (or per host in the inventory) to install the Enterprise build. See `src/pyinfra_openobserve/defaults.py` for other server settings such as `o2_server_http_port` and `o2_server_data_dir`.

Run it with pyinfra:

```shell
uv run --directory example -- pyinfra inventory.py deploy.py -y
```

Once deployed, open `http://<ssh_hostname>:5080` and log in with the root user credentials.
