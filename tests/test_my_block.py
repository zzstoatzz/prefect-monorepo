import pytest
from prefect.blocks.core import Block
from prefect.testing.utilities import prefect_test_harness


@pytest.fixture(autouse=True)
def prefect_db():
    with prefect_test_harness() as harness:
        yield harness


class MyBlock(Block):
    x: int


def test_my_block():
    block = MyBlock(x=1)
    assert block.x == 1
