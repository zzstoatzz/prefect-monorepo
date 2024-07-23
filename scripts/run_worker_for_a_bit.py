import subprocess
import sys

from prefect.utilities.timeout import timeout


def main(timeout_seconds: float = 100.0):
    with timeout(seconds=timeout_seconds):
        subprocess.run(["prefect", "worker", "start", "--pool", "local"], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(float(sys.argv[1]))
    else:
        main()
