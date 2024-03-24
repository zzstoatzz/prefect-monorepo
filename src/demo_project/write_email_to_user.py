import marvin
from prefect import flow
from pydantic import BaseModel, Field


class Email(BaseModel):
    subject: str
    recipient_name: str = Field(description="The full name of the recipient")
    body: str

@marvin.fn(model_kwargs={"temperature": 0.5, "model": "gpt-3.5-turbo"})
def write_welcome_email_to_user(first_name: str, last_name: str, instructions: str) -> Email:
    """write a welcome email to a user based on their name and some instructions"""

@flow(log_prints=True)
def compose_email(first_name: str, last_name: str) -> None:
    """Compose an email to a user"""
    print(f"Composing email for user {first_name} {last_name}")

    email: Email = write_welcome_email_to_user(
        first_name=first_name,
        last_name=last_name,
        instructions="the body should only contain a corny haiku inspired by the user's name"
    )

    print(f"Email composed: {email}")

if __name__ == "__main__":
    compose_email(first_name="John", last_name="Doe")
