"""Contains high-level deploy functions for OpenObserve."""

from pyinfra.api import deploy

from .agent import configure_openobserve_agent, install_openobserve_agent
from .server import configure_openobserve_server, install_openobserve_server


@deploy("Deploy OpenObserve Agent")
def deploy_openobserve_agent(
    otel_url: str,
    username: str,
    password: str,
    primary_templates_path: str | None = None,
) -> None:
    """Deploy the OpenObserve Agent on the host."""
    install_openobserve_agent()
    configure_openobserve_agent(
        otel_url=otel_url,
        username=username,
        password=password,
        primary_templates_path=primary_templates_path,
    )


@deploy("Deploy OpenObserve Server")
def deploy_openobserve_server(
    root_user_email: str,
    root_user_password: str,
    primary_templates_path: str | None = None,
) -> None:
    """Deploy the OpenObserve Server on the host."""
    install_openobserve_server()
    configure_openobserve_server(
        root_user_email=root_user_email,
        root_user_password=root_user_password,
        primary_templates_path=primary_templates_path,
    )
