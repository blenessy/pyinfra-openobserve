# pyinfra-openobserve Example

Example usage of pyinfra-openobserve to deploy the OpenObserve OTEL agent and (optionally) the OpenObserve Server on a remote host.

## Running the example locally

Create `inventory.py` with something like this:

```python
my_servers = [
    (
        "myhost",
        {
            "ssh_hostname": "1.2.3.4",
            "ssh_user": "root",
            # OpenObserve Agent (required)
            "o2_otel_url": "https://eu1-api.openobserve.ai/api/xxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "o2_username": "john@example.com",
            "o2_password": "o2oi_**********************",
            # OpenObserve Server (optional - omit these to deploy the agent only)
            "o2_server_root_user_email": "root@example.com",
            "o2_server_root_user_password": "Complexpass#123",
        },
    )
]
```

The server deploy is opt-in: `deploy.py` only installs the OpenObserve Server when `o2_server_root_user_email` is set for the host. Hosts that should run the agent only can omit both `o2_server_root_user_email` and `o2_server_root_user_password`.

Run it with pyinfra:

```shell
uv run --directory example -- pyinfra inventory.py deploy.py -y
```
