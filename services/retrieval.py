from db.connection import get_connection
from db.models import SAMPLERESULTS_TABLE
import pandas as pd
def retrieve_context(client_name: str, farm_name: str) -> list[str]:
    assert client_name or farm_name, "At least one of client_name or farm_name must be provided"
    conn = get_connection()
    cursor = conn.cursor()

    if client_name and farm_name:
        sql = f"""
            SELECT TOP 100 {",".join([ i for i in SAMPLERESULTS_TABLE['columns'].keys()])} FROM {SAMPLERESULTS_TABLE['name']}
            WHERE client_name = '{client_name}' AND farm_name = '{farm_name}'
            ;
        """
    elif client_name:
        sql = f"""
            SELECT TOP 100 {",".join([ i for i in SAMPLERESULTS_TABLE['columns'].keys()])} FROM {SAMPLERESULTS_TABLE['name']}
            WHERE client_name = '{client_name}
            ;
        """
    elif farm_name:
        sql = f"""
            SELECT TOP 100 {",".join([ i for i in SAMPLERESULTS_TABLE['columns'].keys()])} FROM {SAMPLERESULTS_TABLE['name']}
            WHERE client_name = '{farm_name}
            ;
        """
    df = pd.read_sql(sql, con=conn)
    
    df = df.to_dict("records")
    cursor.close()
    conn.close()
    return df
