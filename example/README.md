# pyinfra-openobserve Example

Example usage of pyinfra-openobserve to deploy OpenObserve OTEL agent on a remote host.

## Running the example locally

Create `inventory.py` with something like this:

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

Run it with pyinfra:

```shell
uv run --directory example -- pyinfra inventory.py deploy.py -y
```
