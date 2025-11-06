"""
Unit tests for the database configuration module.
"""

import pytest
from unittest.mock import patch, MagicMock
import os
from core.database import (
    validate_snowflake_credentials,
    get_snowflake_connection,
    get_connection_params,
    test_connection
)


class TestValidateSnowflakeCredentials:
    """Tests for credential validation."""

    @patch.dict(os.environ, {
        "SNOWFLAKE_ACCOUNT": "test-account",
        "SNOWFLAKE_USER": "test-user",
        "SNOWFLAKE_PASSWORD": "test-password",
        "SNOWFLAKE_ROLE": "test-role",
        "SNOWFLAKE_WAREHOUSE": "test-warehouse",
        "SNOWFLAKE_DATABASE": "test-database",
        "SNOWFLAKE_SCHEMA": "test-schema"
    })
    def test_validate_credentials_success(self):
        """Test successful credential validation."""
        credentials = validate_snowflake_credentials()

        assert credentials["SNOWFLAKE_ACCOUNT"] == "test-account"
        assert credentials["SNOWFLAKE_USER"] == "test-user"
        assert credentials["SNOWFLAKE_PASSWORD"] == "test-password"
        assert credentials["SNOWFLAKE_ROLE"] == "test-role"
        assert credentials["SNOWFLAKE_WAREHOUSE"] == "test-warehouse"
        assert credentials["SNOWFLAKE_DATABASE"] == "test-database"
        assert credentials["SNOWFLAKE_SCHEMA"] == "test-schema"

    @patch.dict(os.environ, {
        "SNOWFLAKE_ACCOUNT": "test-account",
        "SNOWFLAKE_USER": "test-user"
        # Missing other required vars
    })
    def test_validate_credentials_missing_vars(self):
        """Test credential validation with missing environment variables."""
        with pytest.raises(ValueError) as exc_info:
            validate_snowflake_credentials()

        assert "Missing required Snowflake environment variables" in str(exc_info.value)

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_credentials_no_vars(self):
        """Test credential validation with no environment variables."""
        with pytest.raises(ValueError) as exc_info:
            validate_snowflake_credentials()

        assert "Missing required Snowflake environment variables" in str(exc_info.value)


class TestGetSnowflakeConnection:
    """Tests for connection factory."""

    @patch('core.database.snowflake.connector.connect')
    @patch.dict(os.environ, {
        "SNOWFLAKE_ACCOUNT": "test-account",
        "SNOWFLAKE_USER": "test-user",
        "SNOWFLAKE_PASSWORD": "test-password",
        "SNOWFLAKE_ROLE": "test-role",
        "SNOWFLAKE_WAREHOUSE": "test-warehouse",
        "SNOWFLAKE_DATABASE": "test-database",
        "SNOWFLAKE_SCHEMA": "test-schema"
    })
    def test_get_connection_success(self, mock_connect):
        """Test successful connection creation."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = get_snowflake_connection()

        assert conn == mock_conn
        mock_connect.assert_called_once_with(
            account="test-account",
            user="test-user",
            password="test-password",
            role="test-role",
            warehouse="test-warehouse",
            database="test-database",
            schema="test-schema"
        )

    @patch('core.database.snowflake.connector.connect')
    @patch.dict(os.environ, {}, clear=True)
    def test_get_connection_missing_credentials(self, mock_connect):
        """Test connection creation with missing credentials."""
        with pytest.raises(ValueError):
            get_snowflake_connection()

        mock_connect.assert_not_called()


class TestGetConnectionParams:
    """Tests for connection parameters getter."""

    @patch.dict(os.environ, {
        "SNOWFLAKE_ACCOUNT": "test-account",
        "SNOWFLAKE_USER": "test-user",
        "SNOWFLAKE_PASSWORD": "test-password",
        "SNOWFLAKE_ROLE": "test-role",
        "SNOWFLAKE_WAREHOUSE": "test-warehouse",
        "SNOWFLAKE_DATABASE": "test-database",
        "SNOWFLAKE_SCHEMA": "test-schema"
    })
    def test_get_connection_params_success(self):
        """Test successful retrieval of connection parameters."""
        params = get_connection_params()

        assert params["account"] == "test-account"
        assert params["user"] == "test-user"
        assert params["password"] == "test-password"
        assert params["role"] == "test-role"
        assert params["warehouse"] == "test-warehouse"
        assert params["database"] == "test-database"
        assert params["schema"] == "test-schema"


class TestTestConnection:
    """Tests for connection testing."""

    @patch('core.database.get_snowflake_connection')
    def test_connection_success(self, mock_get_conn):
        """Test successful connection test."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = test_connection()

        assert result is True
        mock_cursor.execute.assert_called_once_with("SELECT 1")
        mock_cursor.fetchone.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('core.database.get_snowflake_connection')
    def test_connection_failure(self, mock_get_conn):
        """Test connection test failure."""
        mock_get_conn.side_effect = Exception("Connection failed")

        result = test_connection()

        assert result is False
