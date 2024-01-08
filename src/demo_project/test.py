import emoji
from prefect import flow
from prefect.deployments import DeploymentImage


@flow(log_prints=True)
def random_flow():
    print(emoji.emojize("Hello world :sun_with_face:"))

if __name__ == "__main__":
    random_flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/test.py:random_flow",
    ).deploy(
        "test-k8s",
        work_pool_name="k8s",
        image=DeploymentImage(
            name="docker.io/zzstoatzz/prefect-monorepo",
            dockerfile="Dockerfile.test",
        ),
    )