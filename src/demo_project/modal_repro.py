from prefect import flow


@flow
def hello():
    print("Hello, world!")


if __name__ == "__main__":
    hello.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/modal_repro.py:hello",
    ).deploy(
        name="hello",
        build=False,
        push=False,
        work_pool_name="modal-pipeline-pool",
    )
