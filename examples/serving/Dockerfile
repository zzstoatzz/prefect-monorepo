FROM python:3.12.7-slim

RUN pip install prefect==3.1.0

CMD prefect server database downgrade -y --revision base && \
    prefect server database upgrade -y
