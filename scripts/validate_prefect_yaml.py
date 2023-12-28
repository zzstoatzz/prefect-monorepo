import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, patch

import yaml
from prefect.cli.root import app
from prefect.client.schemas.actions import DeploymentCreate
from pydantic import parse_obj_as


def log_mock_call(method_name, *args, **kwargs):
    print(f"Mocked {method_name} called with args: {args}, kwargs: {kwargs}")

def validate_deployment(**create_deployment_kwargs):
    create_deployment_kwargs |= {"flow_id": uuid.uuid4()} # hmm TODO, revisit
    print(
        json.dumps(
            parse_obj_as(
                DeploymentCreate, create_deployment_kwargs
            ).dict(json_compatible=True),
            indent=2
        )
    )

@asynccontextmanager
async def mock_client(*args, **kwargs):
    mock = AsyncMock()
    
    mock.create_deployment = AsyncMock(side_effect=validate_deployment)

    yield mock
    
async def run_deploy_command():
    with patch(
        'prefect.client.orchestration.PrefectClient',
        new_callable=lambda: mock_client
    ), patch(
        'prefect.deployments.steps.core.run_step',
        AsyncMock(side_effect=lambda *a, **kw: log_mock_call('run_step', *a, **kw))
    ):
        await app(["--no-prompt", "deploy", "--all"], standalone_mode=False)


if __name__ == "__main__":
    with open(Path(__file__).parent.parent / 'prefect.yaml', 'r') as file:
        yaml.safe_load(file)
    asyncio.run(run_deploy_command())