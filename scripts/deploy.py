from pathlib import Path

from prefect import deploy, flow
from prefect.deployments.base import _search_for_flow_functions


async def main(src_dir: Path, bucket: str):
    flow_definitions = await _search_for_flow_functions(str(src_dir))
    deployments = []
    for flow_def in flow_definitions:
        entrypoint = Path(flow_def.get("filepath")).relative_to(src_dir)
        if not str(entrypoint).startswith("build/"):
            deployments.append(
                (
                    await flow.from_source(
                        source=f"s3://{bucket}", entrypoint=entrypoint)
                ).to_deployment()
            )
    await deploy(*deployments)

if __name__ == "__main__":
    import asyncio
    asyncio.run(
        main(
            src_dir=Path(__file__).parents[1],
            bucket="my-bucket"
        )
    )