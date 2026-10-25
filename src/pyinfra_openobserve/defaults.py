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
    "o2_server_version": "1.1.2",
    # NOTE: "opensource" is the AGPL build; "enterprise" is the Enterprise build (free up to 50 GB/day ingestion)
    "o2_server_edition": "opensource",
    "o2_server_download_base_url": "https://downloads.openobserve.ai/releases",
    # SHA256 sums from the official <tarball>.sha256sum files, keyed by edition, OS and arch
    "o2_server_sha256sums": {
        "opensource": {
            "linux": {
                "amd64": "225883447a9e3c75cb52d5a64ece8618cf0d8f3d2eb0b424eebb2e51b0126faa",
                "arm64": "4d00e03155594dba473202fdca4f2b8c3b549138f9bab4ff0f6894feda4b7354",
            },
            "darwin": {
                "amd64": "196861f7beadb533be782f2d98e5458a9a8c383e802f0d108115eddb296cc2f4",
                "arm64": "7914ece4258747ec569504f80f370292f2706112defeb555e6c4e731fd518e45",
            },
        },
        "enterprise": {
            "linux": {
                "amd64": "7d1e3d838a3361e404f0cac518c52deeed3451828fcf702710bffe8b21904634",
                "arm64": "8e2d8c1342f68847a12917c69cea577a08a69c70c2b825511798ca5bc630bebb",
            },
            "darwin": {
                "arm64": "2ffe3f374def1c94f4244d29490c71527908a6404f7e37683a91a83854f5968c",
            },
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
