from prefect import flow
from pydantic import BaseModel


class Plumbus(BaseModel):
    size: str
    color: str

@flow
def use_plumbus(plumbus: Plumbus) -> None:
    print(f"Using plumbus of size {plumbus.size} and color {plumbus.color}")