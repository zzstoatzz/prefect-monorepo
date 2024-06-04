import os

from prefect import flow
from prefect.deployments import DeploymentImage


@flow(log_prints=True)
def say_you_are_healthy():
    print("I am healthy!")
    print(os.environ["FOO"])


if __name__ == "__main__":
    say_you_are_healthy.deploy(
        name="health-check",
        work_pool_name="docker-work",
        image=DeploymentImage(
            name="zzstoatzz/health-check:latest",
            dockerfile="Dockerfile.other_base",
        ),
        job_variables={"env": {"FOO": "bar"}},
        build=False,
        push=False,
    )
