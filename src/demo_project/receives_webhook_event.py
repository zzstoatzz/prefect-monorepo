from prefect import flow


@flow
def handle_webhook_event(id: str, first_name: str, last_name: str) -> None:
    print(f"Received webhook event for {first_name} {last_name} with id {id}")
