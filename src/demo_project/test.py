
from prefect import flow, task


@task
def some_random_task(message: str = "Hello from dev"):
    print(message)
    return message

@flow(log_prints=True)
def random_flow():
    some_random_task()