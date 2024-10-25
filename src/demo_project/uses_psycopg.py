import psycopg2
from prefect import flow


@flow
def get_data_from_postgres():
    psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="postgres",
    )
