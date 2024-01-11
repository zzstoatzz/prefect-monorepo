from prefect import flow


@flow(log_prints=True)
def uses_relative_helper() -> int:
    from .helpers import helper

    return helper()

if __name__ == "__main__":
    uses_relative_helper.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/relative_import_deps.py",
    ).deploy(
        "uses-relative-helper",
        work_pool_name="k8s",
        build=False,
    )