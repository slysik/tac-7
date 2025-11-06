"""
Database configuration and connection management for Snowflake.

This module provides utilities for establishing and managing connections to Snowflake,
including credential validation and connection factory functions.
"""

import os
from typing import Any, Dict
import snowflake.connector
from snowflake.connector import SnowflakeConnection


def validate_snowflake_credentials() -> Dict[str, str]:
    """
    Validate that all required Snowflake credentials are present in environment variables.

    Returns:
        Dict[str, str]: Dictionary containing validated credentials

    Raises:
        ValueError: If any required credential is missing
    """
    required_vars = [
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ROLE",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA"
    ]

    credentials = {}
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            credentials[var] = value

    if missing_vars:
        raise ValueError(
            f"Missing required Snowflake environment variables: {', '.join(missing_vars)}"
        )

    return credentials


def get_snowflake_connection() -> SnowflakeConnection:
    """
    Create and return a new Snowflake database connection.

    Reads credentials from environment variables and establishes a connection
    to the configured Snowflake account, database, and schema.

    Returns:
        SnowflakeConnection: Active Snowflake connection

    Raises:
        ValueError: If required credentials are missing
        snowflake.connector.Error: If connection fails
    """
    credentials = validate_snowflake_credentials()

    connection = snowflake.connector.connect(
        account=credentials["SNOWFLAKE_ACCOUNT"],
        user=credentials["SNOWFLAKE_USER"],
        password=credentials["SNOWFLAKE_PASSWORD"],
        role=credentials["SNOWFLAKE_ROLE"],
        warehouse=credentials["SNOWFLAKE_WAREHOUSE"],
        database=credentials["SNOWFLAKE_DATABASE"],
        schema=credentials["SNOWFLAKE_SCHEMA"]
    )

    return connection


def get_connection_params() -> Dict[str, Any]:
    """
    Get Snowflake connection parameters as a dictionary.

    Useful for passing to pandas or other libraries that accept connection parameters.

    Returns:
        Dict[str, Any]: Connection parameters dictionary

    Raises:
        ValueError: If required credentials are missing
    """
    credentials = validate_snowflake_credentials()

    return {
        "account": credentials["SNOWFLAKE_ACCOUNT"],
        "user": credentials["SNOWFLAKE_USER"],
        "password": credentials["SNOWFLAKE_PASSWORD"],
        "role": credentials["SNOWFLAKE_ROLE"],
        "warehouse": credentials["SNOWFLAKE_WAREHOUSE"],
        "database": credentials["SNOWFLAKE_DATABASE"],
        "schema": credentials["SNOWFLAKE_SCHEMA"]
    }


def test_connection() -> bool:
    """
    Test the Snowflake connection by attempting to connect and execute a simple query.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False
