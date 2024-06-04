import os

import marvin
from prefect import flow
from prefect.deployments import DeploymentImage


@flow(log_prints=True)
def say_you_are_healthy(in_the_style_of: str):
    message = marvin.generate(
        str, instructions=f"Say 'I am healthy' in the style of {in_the_style_of}"
    )

    print(message)


if __name__ == "__main__":
    say_you_are_healthy.deploy(
        name="fun-health-check",
        work_pool_name="docker-work",
        image=DeploymentImage(
            name="zzstoatzz/marvin-fun-health-check:latest",
            dockerfile="Dockerfile.other_base",
        ),
        job_variables={
            "env": {
                "OPENAI_API_KEY": f"{os.getenv('OPENAI_API_KEY')}",
            }
        },
    )
