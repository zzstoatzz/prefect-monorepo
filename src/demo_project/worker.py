from typing import Type

from anyio.abc._tasks import TaskStatus as TaskStatus
from prefect.client.schemas.objects import FlowRun
from prefect.workers.base import (
    BaseJobConfiguration,
    BaseVariables,
    BaseWorker,
    BaseWorkerResult,
)
from prefect_snowflake import SnowflakeCredentials
from pydantic import Field


class DemoWorkerResult(BaseWorkerResult):
    pass


class DemoJobConfiguration(BaseJobConfiguration):
    snowflake_credentials: SnowflakeCredentials = Field(
        ..., description="Snowflake credentials"
    )


class DemoVariables(BaseVariables):
    snowflake_credentials: SnowflakeCredentials = Field(
        ..., description="Snowflake credentials"
    )


class DemoWorker(BaseWorker):
    type: str = "demo"
    job_configuration: Type[BaseJobConfiguration] = DemoJobConfiguration
    job_configuration_variables: Type[BaseVariables] = DemoVariables

    async def run(
        self,
        flow_run: FlowRun,
        configuration: BaseJobConfiguration,
        task_status: TaskStatus | None = None,
    ) -> BaseWorkerResult:
        return DemoWorkerResult(identifier=str(flow_run.id), status_code=0)
