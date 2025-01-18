from typing import Annotated

import pandas as pd
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
    print(flow_input)
    print(num)
    print(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))


if __name__ == "__main__":
    process_input.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/validating_types.py:process_input",
    ).deploy(
        name="process_input",
        parameters=dict(
            flow_input={
                "user": {"name": "John", "age": 30},
                "other_user": {"name": "Jane", "age": 25},
            },
            num=0,
        ),
        job_variables=dict(
            image="prefecthq/prefect:3-latest",
            env=dict(
                EXTRA_PIP_PACKAGES="git+https://github.com/prefecthq/prefect.git@better-load-logging"
            ),
        ),
        work_pool_name="docker-work",
    )
