from datetime import datetime, timedelta

from prefect import flow, task


@task
def get_time_range(start, end) -> tuple[datetime, datetime]:
    return (
        start or datetime.utcnow() - timedelta(days=1),
        end or datetime.utcnow()
    )
    
@flow(retries=1)
def daily_flow(start: datetime | None = None, end: datetime | None = None):
    start, end = get_time_range(start, end)
    print(f"Running daily flow from {start} to {end}...")

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/daily_flow.py:daily_flow"
    ).deploy(
        name=__file__,
        schedule={"cron": "0 14 * * *"}, # 8am CST
        work_pool_name="local"
    )