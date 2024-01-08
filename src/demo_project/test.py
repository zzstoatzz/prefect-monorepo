import emoji
from prefect import flow


@flow(log_prints=True)
def random_flow():
    print(emoji.emojize("Hello world :sun_with_face:"))

if __name__ == "__main__":
    random_flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/test.py:random_flow",
    ).deploy(
        __file__,
        work_pool_name="k8s",
    )