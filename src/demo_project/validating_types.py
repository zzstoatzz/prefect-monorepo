from typing import Annotated

from prefect import flow
from pydantic import BaseModel, Field

NonNegativeInt = Annotated[int, Field(ge=0)]


class User(BaseModel):
    name: str
    age: NonNegativeInt


class FlowInput(BaseModel):
    user: User
    other_user: User


@flow
def process_input(flow_input: FlowInput, num: NonNegativeInt):
    pass


if __name__ == "__main__":
    process_input(
        flow_input={
            "user": {"name": "John", "age": 30},
            "other_user": {"name": "Jane", "age": 25},
        },
        num=-1,
    )
