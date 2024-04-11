from prefect import deploy, flow
from prefect.deployments import DeploymentImage


@flow
def one_flow():
    pass


@flow
def two_flow():
    pass


DOCKER_IMAGE_NAME = "foobar"

if __name__ == "__main__":
    deploy(
        *[
            f.to_deployment(
                name=f"{f.name}-deploy",
                job_variables={"image": DOCKER_IMAGE_NAME},
            )
            for f in [one_flow, two_flow]
        ],
        work_pool_name="docker-work",
        image=DeploymentImage(name=DOCKER_IMAGE_NAME, dockerfile="Dockerfile.demo"),
        push=False,
    )
