import platform
import sys

import prefect
from prefect import flow, task
from prefect.server.api.server import SERVER_API_VERSION
from prefect.states import Completed


@task
def log_platform_info():
    print(
        f"Host's network name = {platform.node()}\n"
        f"Python version = {platform.python_version()}\n"
        f"Platform information (instance type) = {platform.platform()}\n"
        f"OS/Arch = {sys.platform}/{platform.machine()}\n"
        f"Prefect Version = {prefect.__version__} 🚀\n"
        f"Prefect API Version = {SERVER_API_VERSION}\n"
    )

@flow(log_prints=True)
def healthcheck(message: str = "hello, world!"):
    
    print(message)
    
    log_platform_info()

    return Completed(message="Healthcheck completed.")

if __name__ == "__main__":
    healthcheck()