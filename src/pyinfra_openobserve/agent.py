"""Contains low-level OpenObserve Agent deploy functions."""

import base64
import os

from pyinfra import host
from pyinfra.api import DeployError, deploy
from pyinfra.facts.files import Sha256File
from pyinfra.facts.server import Arch, Os
from pyinfra.operations import files, python, server, systemd

from .defaults import DEFAULTS


def raise_deploy_error(message: str) -> None:
    """Raise a DeployError with the given message."""
    raise DeployError(message)


def otel_auth_header(username: str, password: str) -> str:
    """Generate the OTel auth header from the username and password."""
    userpass = f"{username}:{password}"
    token = base64.b64encode(userpass.encode()).decode()
    return f"Basic {token}"


def find_template(name: str, primary_templates_path: str | None) -> str:
    """
    Find the template with the give file name.

    primary_templates_path is prioritized over the default templates path if given.
    """
    if primary_templates_path:
        template_path = os.path.join(primary_templates_path, name)
        if os.path.exists(template_path):
            return template_path
    fallback_templates_path = os.path.join(os.path.dirname(__file__), "templates")
    return os.path.join(fallback_templates_path, name)


@deploy("Install OpenObserve Agent", data_defaults=DEFAULTS)
def install_openobserve_agent() -> None:
    """Install the OpenObserve Agent using the OTel collector contrib package."""
    if not host.data.o2_agent_otelcol_version:
        raise_deploy_error("o2_agent_otelcol_version is not set for this host")

    # set host data
    host.data.o2_agent_otelcol_arch = {
        "x86_64": "amd64",
        "aarch64": "arm64",
    }.get(host.get_fact(Arch), host.get_fact(Arch))
    host.data.o2_agent_otelcol_os = host.get_fact(Os).lower()
    host.data.o2_agent_otel_dir_name = "otelcol-contrib_{}_{}_{}".format(
        host.data.o2_agent_otelcol_version,
        host.data.o2_agent_otelcol_os,
        host.data.o2_agent_otelcol_arch,
    )
    host.data.o2_agent_otel_tarball_name = "{}.tar.gz".format(
        host.data.o2_agent_otel_dir_name,
    )
    host.data.o2_agent_otel_download_url = "{}/v{}/{}".format(
        host.data.o2_agent_otelcol_download_base_url,
        host.data.o2_agent_otelcol_version,
        host.data.o2_agent_otel_tarball_name,
    )
    host.data.o2_agent_cache_dir = os.path.join(
        host.data.o2_agent_home,
        ".cache",
        "openobserve-agent",
    )
    host.data.o2_agent_otel_tarball_path = os.path.join(
        host.data.o2_agent_cache_dir,
        host.data.o2_agent_otel_tarball_name,
    )
    host.data.o2_agent_otel_cache_dir = os.path.join(
        host.data.o2_agent_cache_dir,
        host.data.o2_agent_otel_dir_name,
    )

    server.user(
        name="Create the openobserve-agent user",
        user=host.data.o2_agent_user,
        shell=host.data.o2_agent_shell,
        home=host.data.o2_agent_home,
        create_home=True,
        groups=host.data.o2_agent_groups,
    )

    files.directory(
        name=f"Ensure that {host.data.o2_agent_otel_cache_dir} exists",
        path=host.data.o2_agent_otel_cache_dir,
        user=host.data.o2_agent_user,
        group=host.data.o2_agent_user,
    )

    files.download(
        name="Download OpenTelemetry collector",
        src=host.data.o2_agent_otel_download_url,
        dest=host.data.o2_agent_otel_tarball_path,
        user=host.data.o2_agent_user,
        group=host.data.o2_agent_user,
    )

    expected_sha256 = host.data.o2_agent_otelcol_sha256sums.get(
        host.data.o2_agent_otelcol_os,
    ).get(host.data.o2_agent_otelcol_arch)
    if expected_sha256:
        actual_sha256 = host.get_fact(
            Sha256File,
            path=host.data.o2_agent_otel_tarball_path,
        )
        python.call(
            name="Check OpenTelemetry collector SHA256",
            function=lambda: raise_deploy_error(
                f"OpenTelemetry collector SHA256 mismatch: expected {expected_sha256}, got {actual_sha256}!",
            ),
            _if=lambda: expected_sha256 != actual_sha256,
        )

    files.directory(
        name=f"Ensure that {host.data.o2_agent_cache_dir} exists",
        path=host.data.o2_agent_cache_dir,
        user=host.data.o2_agent_user,
        group=host.data.o2_agent_user,
    )

    files.unarchive(
        name="Extract OpenTelemetry collector",
        src=host.data.o2_agent_otel_tarball_path,
        dest=host.data.o2_agent_otel_cache_dir,
        creates=os.path.join(host.data.o2_agent_otel_cache_dir, "otelcol-contrib"),
        remote_src=True,
        user=host.data.o2_agent_user,
        group=host.data.o2_agent_user,
    )

    files.link(
        name="Create otelcol-contrib symling",
        path=os.path.join(host.data.o2_agent_home, "bin", "otelcol-contrib"),
        target=os.path.join(host.data.o2_agent_otel_cache_dir, "otelcol-contrib"),
        create_remote_dir=True,
        user=host.data.o2_agent_user,
        group=host.data.o2_agent_user,
    )


@deploy("Install OpenObserve Agent", data_defaults=DEFAULTS)
def configure_openobserve_agent(
    otel_url: str,
    username: str,
    password: str,
    primary_templates_path: str | None = None,
) -> None:
    """Configure the OpenObserve Agent on the host."""
    otel_config = files.template(
        name="Upload otel-config.yaml",
        src=find_template("otel-config.yaml", primary_templates_path=primary_templates_path),
        dest=os.path.join(host.data.o2_agent_home, "etc", "otel-config.yaml"),
        o2_otel_url=otel_url,
        o2_otel_auth_header=otel_auth_header(username, password),
        host_data=host.data,  # allow the template to reference host data
    )

    service_config = files.template(
        name="Upload otel-collector.service",
        src=find_template("otel-collector.service", primary_templates_path=primary_templates_path),
        dest="/etc/systemd/system/otel-collector.service",
        o2_agent_home=host.data.o2_agent_home,
        o2_agent_user=host.data.o2_agent_user,
        host_data=host.data,  # allow the template to reference host data
    )

    systemd.service(
        name="Ensure that otel-collector service is running and enabled",
        service="otel-collector",
        running=True,
        enabled=True,
    )

    systemd.service(
        name="Restart the otel-collector service",
        service="otel-collector",
        running=True,
        enabled=True,
        daemon_reload=True,
        restarted=True,
        _if=lambda: otel_config.did_change() or service_config.did_change(),
    )

    # TODO: wait for service to be running but dont use netstat
