import os

from pyinfra import host
from pyinfra_openobserve import deploy_openobserve_agent

deploy_openobserve_agent(
    otel_url=host.data.o2_otel_url,
    username=host.data.o2_username,
    password=host.data.o2_password,
    primary_templates_path=os.path.join(os.path.dirname(__file__), "templates"),
)
