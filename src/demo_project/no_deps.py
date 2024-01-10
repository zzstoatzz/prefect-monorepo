from prefect import flow


@flow(log_prints=True)
def independent_flow():
    print("i ain't got no dependencies")