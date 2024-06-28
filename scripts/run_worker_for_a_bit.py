import subprocess

from prefect.utilities.timeout import timeout


def main():
    with timeout(100):
        subprocess.run(["prefect", "worker", "start", "--pool", "local"], check=True)


if __name__ == "__main__":
    main()
