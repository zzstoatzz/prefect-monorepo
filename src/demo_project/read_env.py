import os

from prefect import flow


@flow(log_prints=True)
def read_env():
    print(os.environ["MAMBA_ROOT_PREFIX"])