"""Contains low-level OpenObserve Server deploy functions."""

import os

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.files import Sha256File
from pyinfra.facts.server import Arch, Os
from pyinfra.operations import files, python, server, systemd

from .agent import find_template, raise_deploy_error
from .defaults import DEFAULTS


@deploy("Install OpenObserve Server", data_defaults=DEFAULTS)
def install_openobserve_server() -> None:
    """Install the OpenObserve Server using the official OpenObserve binary."""
    if not host.data.o2_server_version:
        raise_deploy_error("o2_server_version is not set for this host")

    # set host data
    host.data.o2_server_arch = {
        "x86_64": "amd64",
        "aarch64": "arm64",
    }.get(host.get_fact(Arch), host.get_fact(Arch))
    host.data.o2_server_os = host.get_fact(Os).lower()
    host.data.o2_server_tarball_name = "openobserve-{}_{}_{}.tar.gz".format(
        host.data.o2_server_version,
        host.data.o2_server_os,
        host.data.o2_server_arch,
    )
    host.data.o2_server_download_url = "{}/{}/{}/{}".format(
        host.data.o2_server_download_base_url,
        host.data.o2_server_edition,
        host.data.o2_server_version,
        host.data.o2_server_tarball_name,
    )
    host.data.o2_server_cache_dir = os.path.join(
        host.data.o2_server_home,
        ".cache",
        "openobserve-server",
    )
    host.data.o2_server_tarball_path = os.path.join(
        host.data.o2_server_cache_dir,
        host.data.o2_server_tarball_name,
    )
    host.data.o2_server_bin_cache_dir = os.path.join(
        host.data.o2_server_cache_dir,
        "openobserve-{}_{}_{}".format(
            host.data.o2_server_version,
            host.data.o2_server_os,
            host.data.o2_server_arch,
        ),
    )

    server.user(
        name="Create the openobserve-server user",
        user=host.data.o2_server_user,
        shell=host.data.o2_server_shell,
        home=host.data.o2_server_home,
        create_home=True,
    )

    files.directory(
        name=f"Ensure that {host.data.o2_server_bin_cache_dir} exists",
        path=host.data.o2_server_bin_cache_dir,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    files.download(
        name="Download OpenObserve server",
        src=host.data.o2_server_download_url,
        dest=host.data.o2_server_tarball_path,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    expected_sha256 = host.data.o2_server_sha256sums.get(
        host.data.o2_server_os,
    ).get(host.data.o2_server_arch)
    if expected_sha256:
        actual_sha256 = host.get_fact(
            Sha256File,
            path=host.data.o2_server_tarball_path,
        )
        python.call(
            name="Check OpenObserve server SHA256",
            function=lambda: raise_deploy_error(
                f"OpenObserve server SHA256 mismatch: expected {expected_sha256}, got {actual_sha256}!",
            ),
            _if=lambda: expected_sha256 != actual_sha256,
        )

    files.directory(
        name=f"Ensure that {host.data.o2_server_cache_dir} exists",
        path=host.data.o2_server_cache_dir,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    files.unarchive(
        name="Extract OpenObserve server",
        src=host.data.o2_server_tarball_path,
        dest=host.data.o2_server_bin_cache_dir,
        creates=os.path.join(host.data.o2_server_bin_cache_dir, "openobserve"),
        remote_src=True,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    files.link(
        name="Create openobserve symlink",
        path=os.path.join(host.data.o2_server_home, "bin", "openobserve"),
        target=os.path.join(host.data.o2_server_bin_cache_dir, "openobserve"),
        create_remote_dir=True,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    files.directory(
        name=f"Ensure that {host.data.o2_server_data_dir} exists",
        path=host.data.o2_server_data_dir,
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )


@deploy("Install OpenObserve Server", data_defaults=DEFAULTS)
def configure_openobserve_server(
    root_user_email: str,
    root_user_password: str,
    primary_templates_path: str | None = None,
) -> None:
    """Configure the OpenObserve Server on the host."""
    env_file = os.path.join(host.data.o2_server_home, "etc", "openobserve.env")

    env_config = files.template(
        name="Upload openobserve.env",
        src=find_template("openobserve.env", primary_templates_path=primary_templates_path),
        dest=env_file,
        o2_server_root_user_email=root_user_email,
        o2_server_root_user_password=root_user_password,
        host_data=host.data,  # allow the template to reference host data
        mode="0640",
        user=host.data.o2_server_user,
        group=host.data.o2_server_group,
    )

    service_config = files.template(
        name="Upload openobserve.service",
        src=find_template("openobserve.service", primary_templates_path=primary_templates_path),
        dest="/etc/systemd/system/openobserve.service",
        o2_server_home=host.data.o2_server_home,
        o2_server_user=host.data.o2_server_user,
        o2_server_group=host.data.o2_server_group,
        o2_server_env_file=env_file,
        host_data=host.data,  # allow the template to reference host data
    )

    systemd.service(
        name="Ensure that openobserve service is running and enabled",
        service="openobserve",
        running=True,
        enabled=True,
    )

    systemd.service(
        name="Restart the openobserve service",
        service="openobserve",
        running=True,
        enabled=True,
        daemon_reload=True,
        restarted=True,
        _if=lambda: env_config.did_change() or service_config.did_change(),
    )

    # TODO: wait for service to be running but dont use netstat
