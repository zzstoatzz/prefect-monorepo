import pathlib
from prefect.deployments.base import _search_for_flow_functions

async def main():
    base_dir = pathlib.Path(__file__).parent.parent
    entrypoints = [
        f"{pathlib.Path(flow['filepath']).relative_to(base_dir)}:{flow['function_name']}"
        for flow in await _search_for_flow_functions(directory=str(base_dir))
    ]
    print(','.join(entrypoints))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
