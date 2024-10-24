"""Demonstrate how to dynamically set the start and end datetimes of a flow
that runs daily, and illustrates that retries will occur with the same inputs.

```python
    # Deploying the flow
    flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/daily_flow.py:daily_flow"
    ).deploy(
        name="My Daily Flow Deployment",
        schedule={"cron": "0 14 * * *"},
        work_pool_name="prefect-managed"
    )
```
"""

from datetime import datetime, timedelta

from prefect import flow, task
from prefect.client.schemas.schedules import CronSchedule
from prefect.context import get_run_context


@task  # doesn't need to be a task, but just to be conspicious
def get_time_range(
    start: datetime | None = None, end: datetime | None = None, lookback_days: int = 1
) -> tuple[datetime, datetime]:
    """Get time range start and end datetimes, default is past 24 hours."""
    if start and end and start >= end:
        raise ValueError("start must precede end")
    return (
        start or (now := datetime.utcnow()) - timedelta(days=lookback_days),
        end or now,
    )


@flow(retries=1)
def downstream_workflow(start: datetime, end: datetime):
    # globals not recommended, we're just showing that retries occur with same inputs
    global data
    data.update({(start, end): get_run_context().flow_run.run_count})
    print(f"Running downstream workflow from {start} to {end}...")
    raise ValueError("oops i failed this time")


@flow(log_prints=True)
def daily_flow(start: datetime | None = None, end: datetime | None = None):
    start, end = get_time_range(start, end)

    global data  # again, avoid globals in practice, use redis or something
    data = dict()

    downstream_workflow(start, end, return_state=True)  # return state to avoid raising

    used_one_dt_range = len(data) == 1 and data.keys() == {(start, end)}
    ran_subflow_twice = data.get((start, end)) == 2

    if used_one_dt_range and ran_subflow_twice:
        return "Failed successfully!"


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/daily_flow.py:daily_flow",
    ).deploy(
        name="My Daily Flow Deployment",
        schedules=[CronSchedule(cron="0 14 * * *", timezone="America/Chicago")],
        work_pool_name="local",
    )
