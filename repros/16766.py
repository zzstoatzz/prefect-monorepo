# /// script
# dependencies = ["prefect-ray"]
# ///

import time

from prefect import flow, task
from prefect_ray.task_runners import RayTaskRunner


@task(name="test_task")
def test_run():
    time.sleep(10)


@flow(task_runner=RayTaskRunner())
def my_flow():
    test_run_result = test_run.submit()
    return test_run_result


if __name__ == "__main__":
    print(my_flow())
