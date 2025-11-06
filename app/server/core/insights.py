from typing import List, Optional
from snowflake.connector import DictCursor
from core.data_models import ColumnInsight
from .database import get_snowflake_connection
from .sql_security import (
    execute_query_safely,
    validate_identifier,
    SQLSecurityError
)

def generate_insights(table_name: str, column_names: Optional[List[str]] = None) -> List[ColumnInsight]:
    """
    Generate statistical insights for table columns using Snowflake
    """
    try:
        # Validate table name
        validate_identifier(table_name, "table")

        conn = get_snowflake_connection()

        # Get table schema using INFORMATION_SCHEMA
        cursor_info = execute_query_safely(
            conn,
            """SELECT COLUMN_NAME, DATA_TYPE
               FROM INFORMATION_SCHEMA.COLUMNS
               WHERE TABLE_SCHEMA = CURRENT_SCHEMA()
               AND TABLE_NAME = {table}""",
            identifier_params={'table': table_name.upper()}
        )
        columns_info = cursor_info.fetchall()
        
        # If no specific columns requested, analyze all
        if not column_names:
            column_names = [col[0] for col in columns_info]
        else:
            # Validate provided column names
            for col in column_names:
                try:
                    validate_identifier(col, "column")
                except SQLSecurityError:
                    raise Exception(f"Invalid column name: {col}")

        insights = []

        for col_info in columns_info:
            col_name = col_info[0]
            col_type = col_info[1]
            
            if col_name not in column_names:
                continue
            
            # Validate column name
            try:
                validate_identifier(col_name, "column")
            except SQLSecurityError:
                # Skip columns with invalid names
                continue
            
            # Basic statistics using safe query execution
            cursor_distinct = execute_query_safely(
                conn,
                "SELECT COUNT(DISTINCT {column}) FROM {table}",
                identifier_params={'column': col_name, 'table': table_name.upper()}
            )
            unique_values = cursor_distinct.fetchone()[0]

            cursor_null = execute_query_safely(
                conn,
                "SELECT COUNT(*) FROM {table} WHERE {column} IS NULL",
                identifier_params={'table': table_name.upper(), 'column': col_name}
            )
            null_count = cursor_null.fetchone()[0]
            
            insight = ColumnInsight(
                column_name=col_name,
                data_type=col_type,
                unique_values=unique_values,
                null_count=null_count
            )
            
            # Type-specific insights
            # Snowflake numeric types: NUMBER, DECIMAL, NUMERIC, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT, FLOAT, DOUBLE
            if col_type in ['NUMBER', 'DECIMAL', 'NUMERIC', 'INT', 'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT', 'BYTEINT', 'FLOAT', 'DOUBLE', 'REAL']:
                # Numeric insights using safe query execution
                cursor_stats = execute_query_safely(
                    conn,
                    """
                    SELECT
                        MIN({column}) as min_val,
                        MAX({column}) as max_val,
                        AVG({column}) as avg_val
                    FROM {table}
                    WHERE {column} IS NOT NULL
                    """,
                    identifier_params={'column': col_name, 'table': table_name.upper()}
                )
                result = cursor_stats.fetchone()
                if result:
                    insight.min_value = result[0]
                    insight.max_value = result[1]
                    insight.avg_value = result[2]
            
            # Most common values (for all types) using safe query execution
            cursor_common = execute_query_safely(
                conn,
                """
                SELECT {column}, COUNT(*) as count
                FROM {table}
                WHERE {column} IS NOT NULL
                GROUP BY {column}
                ORDER BY count DESC
                LIMIT 5
                """,
                identifier_params={'column': col_name, 'table': table_name.upper()}
            )
            most_common = cursor_common.fetchall()
            if most_common:
                insight.most_common = [
                    {"value": val, "count": count}
                    for val, count in most_common
                ]

            insights.append(insight)

        conn.close()
        return insights

    except Exception as e:
        raise Exception(f"Error generating insights: {str(e)}")