import platform
import sys
import time

import typer
from prefect import __version__ as PREFECT_SDK_VERSION
from prefect import flow, task
from prefect.blocks.core import Block
from prefect.server.api.server import SERVER_API_VERSION
from prefect.states import Completed
from rich.console import Console

app = typer.Typer()
console = Console()

def ping_if_stale_version(flow, flow_run, state):
    import httpx
    r = httpx.get("https://pypi.org/pypi/prefect/json")
    if (latest_version := r.json()["info"]["version"]) != PREFECT_SDK_VERSION:
        Block.load("slack-webhook/my-webhook").notify(
            f"⚠️  You are running Prefect version {PREFECT_SDK_VERSION}"
            f" however version {latest_version} is available."
        )

@task
def log_platform_info():
    console.print(
        f"\nHost's network name = {platform.node()}\n"
        f"Python version = {platform.python_version()}\n"
        f"Platform information (instance type) = {platform.platform()}\n"
        f"OS/Arch = {sys.platform}/{platform.machine()}\n"
        f"Prefect Version = {PREFECT_SDK_VERSION} 🚀\n"
        f"Prefect API Version = {SERVER_API_VERSION}\n"
    )

@flow(on_completion=[ping_if_stale_version])
def healthcheck(
    message: str,
    introduce_exception: bool = False,
    sleep: int | None = None
) -> Completed:
    console.print(f"{message}")

    if introduce_exception:
        raise ValueError("ooooo noooooo")

    log_platform_info()
    
    if sleep:
        time.sleep(sleep)

    return Completed(message="Healthcheck completed.")

@app.command()
def run_healthcheck(
    message: str = typer.Option("hello, world!", help="Message to display"),
    introduce_exception: bool = typer.Option(False, help="Introduce an exception")
):
    state = healthcheck(
        message=message,
        introduce_exception=introduce_exception,
        return_state=True
    )
    console.print(f"\nHealthcheck final state » {state}\n")

if __name__ == "__main__":
    app()