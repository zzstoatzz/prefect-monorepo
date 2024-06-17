from prefect import flow


@flow(log_prints=True)
def hello_docker():
    """
    A simple flow that prints 'Hello, Docker!' to the logs
    """
    print("Hello, Docker!")


if __name__ == "__main__":
    hello_docker()
