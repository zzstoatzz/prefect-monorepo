FROM prefecthq/prefect:3.0.0-python3.12

ENV UV_SYSTEM_PYTHON=1

COPY api.py .

RUN pip install -U pip uv

RUN uv pip install git+https://github.com/prefecthq/controlflow.git@main


