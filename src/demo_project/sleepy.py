from prefect import flow


@flow
def sleepy():
    import time

    time.sleep(1000)


if __name__ == "__main__":
    sleepy.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/sleepy.py:sleepy",
    ).deploy(
        work_pool_name="local",
    )
