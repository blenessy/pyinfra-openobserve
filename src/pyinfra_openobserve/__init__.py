"""Contains high-level deploy functions for OpenObserve."""

from pyinfra.api import deploy

from .agent import configure_openobserve_agent, install_openobserve_agent


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
