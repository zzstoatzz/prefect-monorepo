from helpers import helper
from prefect import flow


@flow(log_prints=True)
def uses_helper() -> int:
    return helper()

if __name__ == "__main__":
    uses_helper.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/relative_import_deps.py:uses_helper",
    ).deploy(
        "uses-relative-helper",
        work_pool_name="k8s",
        build=False,
    )