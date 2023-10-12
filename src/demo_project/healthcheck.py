import platform
import sys

import prefect
from prefect import flow, task
from prefect.blocks.core import Block
from prefect.results import PersistedResultBlob
from prefect.server.api.server import SERVER_API_VERSION
from prefect.states import Completed


@task(log_prints=True, result_storage_key="healthcheck_message.pkl")
def save_message(message: str):
    print(message)
    return message

def assert_result_saved(
    storage_key: str, storage_block: str = "s3/flow-script-storage"
):
    import base64
    import pickle
    saved_result = pickle.loads(
        base64.b64decode(
            PersistedResultBlob(
                Block.load(storage_block).read_path(storage_key)
            ).data
        )
    )
    assert saved_result == "hello, world!"

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

@flow(log_prints=True, persist_result=True)
def healthcheck(
    message: str = "hello, world!", introduce_exception: bool = False
) -> str:
    
    save_message(message)
    
    assert_result_saved("healthcheck_message.pkl")

    if introduce_exception:
        raise ValueError("ooooo noooooo")

    log_platform_info()

    return Completed(message="Healthcheck completed.")

if __name__ == "__main__":
    state = healthcheck(introduce_exception=True, return_state=True)
    print(state.result())