from prefect import flow
from pydantic import SecretStr


@flow(log_prints=True)
def accepts_secret(secret: SecretStr) -> None:
    print(secret.get_secret_value())

if __name__ == "__main__":
    accepts_secret.serve(name="Accepts Secret")