from prefect import flow
from prefect.client.schemas.schedules import CronSchedule


@flow
def sleepy():
    import time

    time.sleep(1000)


if __name__ == "__main__":
    sleepy.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/sleepy.py:sleepy",
    ).deploy(
        name="sleepy-local",
        work_pool_name="local",
        schedules=[CronSchedule(cron="* * * * *", max_active_runs=1)],
    )
