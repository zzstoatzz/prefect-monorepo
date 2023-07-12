import pathlib
from prefect.deployments.base import _search_for_flow_functions

async def main():
    src_dir = pathlib.Path('src')
    base_dir = pathlib.Path(__file__).resolve().parent.parent / src_dir
    
    entrypoints = [
        f"src/{flow['filepath'].replace(str(base_dir) + '/', '')}:{flow['function_name']}"
        for flow in await _search_for_flow_functions(directory=str(base_dir))
        if str(base_dir) in flow['filepath']
    ]

    print(','.join(entrypoints))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
