from typing import List, Dict
import pandas as pd
import io
from snowflake.connector import SnowflakeConnection


def generate_csv_from_data(data: List[Dict], columns: List[str]) -> bytes:
    """
    Generate CSV file from data and columns.

    Args:
        data: List of dictionaries containing the data
        columns: List of column names

    Returns:
        bytes: CSV file content as bytes
    """
    if not data and not columns:
        return b""

    if not columns and data:
        columns = list(data[0].keys()) if data else []

    df = pd.DataFrame(data, columns=columns)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_content.encode('utf-8')


def generate_csv_from_table(conn: SnowflakeConnection, table_name: str) -> bytes:
    """
    Generate CSV file from a Snowflake database table.

    Args:
        conn: Snowflake database connection
        table_name: Name of the table to export

    Returns:
        bytes: CSV file content as bytes

    Raises:
        ValueError: If table doesn't exist
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as cnt
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = CURRENT_SCHEMA()
        AND TABLE_NAME = %s
    """, (table_name,))

    result = cursor.fetchone()
    if not result or result[0] == 0:
        raise ValueError(f"Table '{table_name}' does not exist")

    query = f'SELECT * FROM "{table_name}"'
    df = pd.read_sql_query(query, conn)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()

    return csv_content.encode('utf-8')