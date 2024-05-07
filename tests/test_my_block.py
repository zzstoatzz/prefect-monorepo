from prefect.blocks.core import Block


class MyBlock(Block):
    x: int


def test_my_block():
    block = MyBlock(x=1)
    assert block.x == 1
