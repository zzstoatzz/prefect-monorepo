import os

from prefect import flow, task


@task
def do_something_important(not_so_secret_value: str) -> None:
    print(f"Doing something important with {not_so_secret_value}!")


@flow(log_prints=True)
def some_work():
    environment = os.environ.get("EXECUTION_ENVIRONMENT", "local")

    print(f"Coming to you live from {environment}!")

    not_so_secret_value = os.environ.get("MY_NOT_SO_SECRET_CONFIG")

    if not_so_secret_value is None:
        raise ValueError("You forgot to set MY_NOT_SO_SECRET_CONFIG!")

    do_something_important(not_so_secret_value)


if __name__ == "__main__":
    some_work.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/demo_flow.py:some_work",
    ).deploy(
        name="demo-deployment",
        work_pool_name="local",
        job_variables={
            "env": {
                "EXECUTION_ENVIRONMENT": "{{ $EXECUTION_ENVIRONMENT }}",
                "MY_NOT_SO_SECRET_CONFIG": "{{ $MY_NOT_SO_SECRET_CONFIG }}",
            }
        },
    )
