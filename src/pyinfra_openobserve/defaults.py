"""Default host.data values for OpenObserve Agent and Server deployments."""

DEFAULTS = {
    "o2_agent_otelcol_version": "0.111.0",
    "o2_agent_otelcol_download_base_url": "https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download",
    "o2_agent_otelcol_sha256sums": {
        "linux": {
            "amd64": "bce8ab7431d25529fb8820f0729c8b60b090d0d7e36b9b668aec88698b64439a",
            "arm64": "67fc192833823dbd4586e10dcfa803ac5c8f82e918785b55fc8684c002e325c5",
        },
        "darwin": {
            "arm64": "e56bf2cb535b6c089915415d2ab5e477c98628d03f3376aaf9124fa4f8b24f97",
        },
    },
    "o2_agent_user": "openobserve-agent",
    # NOTE: this is works for Ubuntu/Debian-based system but may need adjustment for other distributions
    "o2_agent_groups": ["adm", "systemd-journal"],
    "o2_agent_shell": "/bin/sh",
    "o2_agent_home": "/opt/openobserve-agent",
    # OpenObserve Server defaults
    "o2_server_version": "0.91.4",
    # NOTE: edition "o2" is the OSS build; "o2-enterprise" is the Enterprise build (free up to 50 GB/day ingestion)
    "o2_server_edition": "o2",
    "o2_server_download_base_url": "https://downloads.openobserve.ai/releases",
    # TODO: replace the placeholder SHA256 sums with real values from downloads.openobserve.ai
    "o2_server_sha256sums": {
        "linux": {
            "amd64": "<TODO: sha256 for openobserve-0.91.4-linux-amd64.tar.gz>",
            "arm64": "<TODO: sha256 for openobserve-0.91.4-linux-arm64.tar.gz>",
        },
    },
    "o2_server_user": "openobserve-server",
    "o2_server_group": "openobserve-server",
    "o2_server_shell": "/bin/sh",
    "o2_server_home": "/opt/openobserve-server",
    "o2_server_data_dir": "/opt/openobserve-server/data",
    # NOTE: binding to all interfaces is intentional for a network server
    "o2_server_bind_addr": "0.0.0.0",  # noqa: S104
    "o2_server_http_port": 5080,
}
