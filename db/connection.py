import pyodbc
from utils.config import get_db_config
import pandas as pd

def get_connection():
    config = get_db_config()
    connection_string = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={config['DB_HOST']};"
        f"DATABASE={config['DB_DATABASE']};"
        f"UID={config['DB_USER']};"
        f"PWD={config['DB_PASSWORD']}"
    )
    connection = pyodbc.connect(connection_string)
    return connection

def get_data(sql_query):
    conn = get_connection()
    df = pd.read_sql(sql_query, con=conn)
    return df
