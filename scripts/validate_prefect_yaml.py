import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import yaml
from prefect.cli.root import app
from prefect.client.schemas.actions import DeploymentCreate
from pydantic import TypeAdapter


def log_mock_call(method_name: str, *args: Any, **kwargs: Any):
    print(f"Mocked {method_name} called with args: {args}, kwargs: {kwargs}")


def validate_deployment(**create_deployment_kwargs: Any):
    create_deployment_kwargs |= {"flow_id": uuid.uuid4()}  # hmm TODO, revisit
    print(
        TypeAdapter(DeploymentCreate)
        .validate_python(create_deployment_kwargs)
        .model_dump_json(indent=2),
    )


@asynccontextmanager
async def mock_client(*args: Any, **kwargs: Any):
    mock = AsyncMock()

    mock.create_deployment = AsyncMock(side_effect=validate_deployment)

    yield mock


def _side_effect(method_name: str, *args: Any, **kwargs: Any):
    log_mock_call(method_name, *args, **kwargs)


def run_deploy_command():
    with (
        patch(
            "prefect.client.orchestration.PrefectClient",
            new_callable=lambda: mock_client,
        ),
        patch(
            "prefect.deployments.steps.core.run_step",
            AsyncMock(side_effect=_side_effect("run_step")),
        ),
    ):
        app(["--no-prompt", "deploy", "--all"], standalone_mode=False)


if __name__ == "__main__":
    with open(Path(__file__).parent.parent / "prefect.yaml", "r") as file:
        yaml.safe_load(file)
    run_deploy_command()
