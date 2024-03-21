import random
import time

from prefect import task
from prefect.task_server import serve

@task(retries=3)
def do_work(input_: str) -> str:
    if random.random() < 0.5:
        raise ValueError("This is a random failure!")
    time.sleep(random.randint(3, 10))

if __name__ == "__main__":
    serve(do_work)