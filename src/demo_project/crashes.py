from prefect import flow


@flow
def boom_crash():
    raise ValueError


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/crashes.py:boom_crash",
    ).deploy(
        name="boom-crash",
        work_pool_name="local",
    )
