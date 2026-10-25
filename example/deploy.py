"""Example deployment of the OpenObserve OTEL agent and the OpenObserve Server."""

import os

from pyinfra import host

from pyinfra_openobserve import deploy_openobserve_agent, deploy_openobserve_server

primary_templates_path = os.path.join(os.path.dirname(__file__), "templates")

# The server deploy is opt-in: only run when the host provides root credentials
# in its inventory. Agent-only hosts can omit o2_server_root_user_email/password.
# The server is deployed first so that an agent on the same host can ship to it.
if host.data.get("o2_server_root_user_email"):
    deploy_openobserve_server(
        root_user_email=host.data.o2_server_root_user_email,
        root_user_password=host.data.o2_server_root_user_password,
        primary_templates_path=primary_templates_path,
    )

deploy_openobserve_agent(
    otel_url=host.data.o2_otel_url,
    username=host.data.o2_username,
    password=host.data.o2_password,
    primary_templates_path=primary_templates_path,
)
