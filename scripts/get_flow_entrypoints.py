import sys
from prefect.deployments.base import _search_for_flow_functions

def main(filepath):
    entrypoints = [
        f"{flow['filepath']}:{flow['function_name']}"
        for flow in _search_for_flow_functions()
        if flow['filepath'] == filepath
    ]
    print(','.join(entrypoints))

if __name__ == "__main__":
    main(sys.argv[1])
