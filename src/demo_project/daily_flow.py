from datetime import datetime, timedelta

from prefect import flow, task


@task # doesn't need to be a task, but just to be conspicious
def get_time_range(
    start: datetime | None = None,
    end: datetime | None = None,
    lookback_days: int = 1
) -> tuple[datetime, datetime]:
    """Get time range start and end datetimes, default is past 24 hours."""
    if start and end and start >= end:
        raise ValueError("start must precede end")
    return (
        start or (now := datetime.utcnow()) - timedelta(days=lookback_days),
        end or now
    )

@flow(retries=1)
def downstream_workflow(start: datetime, end: datetime):
    global seen_times
    seen_times.add((start, end))
    print(f"Running downstream workflow from {start} to {end}...")
    raise ValueError("oops i failed this time")

@flow(log_prints=True)
def daily_flow(start: datetime | None = None, end: datetime | None = None):
    start, end = get_time_range(start, end)
    
    global seen_times
    seen_times = set()
        
    downstream_workflow(start, end, return_state=True) # return state to avoid raising
        
    assert len(seen_times) == 1 and seen_times.pop() == (start, end)

if __name__ == "__main__":
    daily_flow()
    
    ## Deploying the flow
    # flow.from_source(
    #     source="https://github.com/zzstoatzz/prefect-monorepo.git",
    #     entrypoint="src/demo_project/daily_flow.py:daily_flow"
    # ).deploy(
    #     name="My Daily Flow Deployment",
    #     schedule={"cron": "0 14 * * *"},
    #     work_pool_name="prefect-managed"
    # )