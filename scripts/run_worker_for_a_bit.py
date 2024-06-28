import subprocess

from prefect.utilities.timeout import timeout_async


async def main():
    with timeout_async(100):
        await subprocess.run(
            ["prefect", "worker", "start", "--pool", "local"], check=True
        )
