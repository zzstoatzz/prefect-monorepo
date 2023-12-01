
from prefect import flow, task


@task
def some_random_ish():
    return "Hello world"

@flow(log_prints=True)
def random_flow():
    some_random_ish()