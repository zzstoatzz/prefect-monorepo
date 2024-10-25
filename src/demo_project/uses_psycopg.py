import psycopg
from prefect import flow


@flow
def get_data_from_postgres():
    psycopg.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="postgres",
    )
