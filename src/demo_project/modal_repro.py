from prefect import flow


@flow(log_prints=True)
def hello():
    print("Hello, world!")


if __name__ == "__main__":
    # created work pool with
    # prefect work-pool create --type modal:push --provision-infra modal --overwrite
    hello.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/modal_repro.py:hello",
    ).deploy(
        name="hello",
        build=False,
        push=False,
        work_pool_name="modal",
    )
