import asyncio

from prefect import flow, get_client
from prefect.client.schemas.actions import WorkPoolCreate
from prefect.deployments import run_deployment
from prefect.variables import Variable


@flow
def dummy_flow():
    print("I am a dummy flow")


async def create_work_pool():
    async with get_client() as client:
        await client.create_work_pool(
            WorkPoolCreate(
                name="ecs-work-pool",
                description="A work pool for ECS work",
                base_job_template=dict(
                    variables=dict(
                        type="object", properties=dict(vpc_id=dict(type="string"))
                    ),
                    job_configuration=dict(
                        vpc_id="{{ prefect.variables.some_vpc_id }}"
                    ),
                ),
            )
        )


if __name__ == "__main__":
    Variable.set("some_vpc_id", "vpc-12345678", overwrite=True)
    asyncio.run(create_work_pool())
    dummy_flow.deploy(name="dummy", work_pool_name="ecs-work-pool")
    flow_run = run_deployment("dummy-flow/dummy", timeout=0)
    assert flow_run.job_variables.get("vpc_id") == "vpc-12345678"
