import os

from prefect import flow
from prefect.blocks.system import Secret

secret = Secret(value="my-secret-value")

secret.save("my-secret", overwrite=True, _sync=True)


@flow
def my_flow():
    print(os.environ["MY_SECRET"])
