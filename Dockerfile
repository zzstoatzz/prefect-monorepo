FROM prefecthq/prefect:3.1.4-python3.12
COPY requirements.txt /opt/prefect/prefect-monorepo/requirements.txt
RUN python -m pip install -r /opt/prefect/prefect-monorepo/requirements.txt
COPY . /opt/prefect/prefect-monorepo/
WORKDIR /opt/prefect/prefect-monorepo/
