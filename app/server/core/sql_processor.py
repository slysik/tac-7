from typing import Dict, Any
from snowflake.connector import DictCursor
from .database import get_snowflake_connection
from .sql_security import (
    execute_query_safely,
    validate_sql_query,
    SQLSecurityError
)

def execute_sql_safely(sql_query: str) -> Dict[str, Any]:
    """
    Execute SQL query with safety checks
    """
    try:
        # Validate the SQL query for dangerous operations
        validate_sql_query(sql_query)

        # Connect to Snowflake database
        conn = get_snowflake_connection()

        # Execute query safely with DictCursor to get results as dictionaries
        # Note: Since this is a user-provided complete SQL query,
        # we can't use parameterization. The validate_sql_query
        # function provides protection against dangerous operations.
        cursor = conn.cursor(DictCursor)
        cursor.execute(sql_query)

        # Get results
        rows = cursor.fetchall()

        # Convert rows to dictionaries and extract columns
        results = []
        columns = []

        if rows:
            # DictCursor returns rows as dictionaries
            columns = list(rows[0].keys())
            results = rows

        cursor.close()
        conn.close()

        return {
            'results': results,
            'columns': columns,
            'error': None
        }

    except SQLSecurityError as e:
        return {
            'results': [],
            'columns': [],
            'error': f"Security error: {str(e)}"
        }
    except Exception as e:
        return {
            'results': [],
            'columns': [],
            'error': str(e)
        }

def get_database_schema() -> Dict[str, Any]:
    """
    Get complete database schema information from Snowflake
    """
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor(DictCursor)

        # Get all tables in the current schema using INFORMATION_SCHEMA
        cursor.execute("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = CURRENT_SCHEMA()
            AND TABLE_TYPE = 'BASE TABLE'
        """)
        tables = cursor.fetchall()

        schema = {'tables': {}}

        for table in tables:
            table_name = table['TABLE_NAME']

            try:
                # Get columns for each table using INFORMATION_SCHEMA
                cursor_info = execute_query_safely(
                    conn,
                    """SELECT COLUMN_NAME, DATA_TYPE
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_SCHEMA = CURRENT_SCHEMA()
                       AND TABLE_NAME = {table}""",
                    identifier_params={'table': table_name}
                )
                columns_info = cursor_info.fetchall()

                columns = {}
                for col in columns_info:
                    columns[col[0]] = col[1]  # column_name: data_type

                # Get row count safely
                cursor_count = execute_query_safely(
                    conn,
                    "SELECT COUNT(*) as cnt FROM {table}",
                    identifier_params={'table': table_name}
                )
                row_count = cursor_count.fetchone()[0]

                schema['tables'][table_name] = {
                    'columns': columns,
                    'row_count': row_count
                }

            except SQLSecurityError:
                # Skip tables with invalid names
                continue

        cursor.close()
        conn.close()

        return schema

    except Exception as e:
        return {'tables': {}, 'error': str(e)}