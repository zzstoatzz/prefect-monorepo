import os

import pandas as pd
from prefect import flow, get_run_logger

test_env = os.environ.get("TEST_ENV")


@flow
def main(hello_msg: str):
    logger = get_run_logger()
    test = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    logger.info(hello_msg)
    logger.info(test)
    logger.info(test_env)


if __name__ == "__main__":
    main.serve("Hello World")
