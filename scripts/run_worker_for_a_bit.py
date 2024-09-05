import subprocess
import sys

from prefect.utilities.timeout import timeout


def main(work_pool: str = "local", timeout_seconds: float = 100.0):
    try:
        with timeout(seconds=timeout_seconds):
            subprocess.run(
                ["prefect", "worker", "start", "--pool", work_pool], check=True
            )
    except TimeoutError:
        print("Worker finished")


if __name__ == "__main__":
    main(work_pool=sys.argv[1], timeout_seconds=float(sys.argv[2]))
