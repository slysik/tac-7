import pytest
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_validated_random_query,
    generate_random_query
)
from core.data_models import QueryRequest


class TestSampleQueryValidation:
    """Tests for sample query validation functionality"""

    def test_generate_validated_query_success_first_attempt(self):
        """Test that a query returning results succeeds on first attempt"""
        schema_info = {
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # Setup mocks
                        mock_nl_query.return_value = "Show me all users"
                        mock_sql.return_value = "SELECT * FROM users"
                        mock_execute.return_value = {
                            'results': [{'id': 1, 'name': 'John'}],
                            'columns': ['id', 'name'],
                            'error': None
                        }

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Assertions
                        assert result == "Show me all users"
                        mock_nl_query.assert_called_once()
                        mock_sql.assert_called_once()
                        mock_execute.assert_called_once()

    def test_generate_validated_query_retry_on_empty_results(self):
        """Test that the function retries when query returns no results"""
        schema_info = {
            "tables": [
                {
                    "name": "products",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # First query returns no results, second succeeds
                        mock_nl_query.side_effect = [
                            "Show me products with negative prices",
                            "Show me all products"
                        ]
                        mock_sql.side_effect = [
                            "SELECT * FROM products WHERE price < 0",
                            "SELECT * FROM products"
                        ]
                        mock_execute.side_effect = [
                            {'results': [], 'columns': [], 'error': None},  # No results
                            {'results': [{'id': 1, 'name': 'Widget'}], 'columns': ['id', 'name'], 'error': None}
                        ]

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Assertions
                        assert result == "Show me all products"
                        assert mock_nl_query.call_count == 2
                        assert mock_sql.call_count == 2
                        assert mock_execute.call_count == 2

    def test_generate_validated_query_retry_on_sql_error(self):
        """Test that the function retries when SQL execution fails"""
        schema_info = {
            "tables": [
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "total", "type": "REAL"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # First query has SQL error, second succeeds
                        mock_nl_query.side_effect = [
                            "Show me orders from invalid_column",
                            "Show me all orders"
                        ]
                        mock_sql.side_effect = [
                            "SELECT * FROM orders WHERE invalid_column > 0",
                            "SELECT * FROM orders"
                        ]
                        mock_execute.side_effect = [
                            {'results': [], 'columns': [], 'error': 'no such column: invalid_column'},
                            {'results': [{'id': 1, 'total': 99.99}], 'columns': ['id', 'total'], 'error': None}
                        ]

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Assertions
                        assert result == "Show me all orders"
                        assert mock_nl_query.call_count == 2
                        assert mock_sql.call_count == 2
                        assert mock_execute.call_count == 2

    def test_generate_validated_query_max_attempts_exceeded(self):
        """Test that exception is raised after maximum retry attempts"""
        schema_info = {
            "tables": [
                {
                    "name": "empty_table",
                    "columns": [
                        {"name": "id", "type": "INTEGER"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # All attempts return no results
                        mock_nl_query.return_value = "Show me data"
                        mock_sql.return_value = "SELECT * FROM empty_table"
                        mock_execute.return_value = {
                            'results': [],
                            'columns': [],
                            'error': None
                        }

                        # Call function with max_attempts=3 for faster testing
                        with pytest.raises(Exception, match="Unable to generate a query that returns results after 3 attempts"):
                            generate_validated_random_query(schema_info, max_attempts=3)

                        # Should have tried 3 times
                        assert mock_nl_query.call_count == 3
                        assert mock_sql.call_count == 3
                        assert mock_execute.call_count == 3

    def test_generate_validated_query_with_anthropic(self):
        """Test query validation with Anthropic when OpenAI key is not available"""
        schema_info = {
            "tables": [
                {
                    "name": "customers",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}, clear=True):
            with patch('core.llm_processor.generate_random_query_with_anthropic') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # Setup mocks
                        mock_nl_query.return_value = "List all customers"
                        mock_sql.return_value = "SELECT * FROM customers"
                        mock_execute.return_value = {
                            'results': [{'id': 1, 'name': 'Alice'}],
                            'columns': ['id', 'name'],
                            'error': None
                        }

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Assertions
                        assert result == "List all customers"
                        mock_nl_query.assert_called_once()

    def test_generate_validated_query_exception_during_generation(self):
        """Test handling of exceptions during query generation"""
        schema_info = {
            "tables": [
                {
                    "name": "test_table",
                    "columns": [
                        {"name": "id", "type": "INTEGER"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # First attempt throws exception, second succeeds
                        mock_nl_query.side_effect = [
                            Exception("API error"),
                            "Show me test data"
                        ]
                        mock_sql.return_value = "SELECT * FROM test_table"
                        mock_execute.return_value = {
                            'results': [{'id': 1}],
                            'columns': ['id'],
                            'error': None
                        }

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Should retry after exception and succeed
                        assert result == "Show me test data"
                        assert mock_nl_query.call_count == 2

    def test_generate_random_query_uses_validation(self):
        """Test that generate_random_query router calls validation function"""
        schema_info = {
            "tables": [
                {
                    "name": "items",
                    "columns": [
                        {"name": "id", "type": "INTEGER"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_validated_random_query') as mock_validated:
                mock_validated.return_value = "Show me all items"

                # Call router function
                result = generate_random_query(schema_info)

                # Assertions
                assert result == "Show me all items"
                mock_validated.assert_called_once_with(schema_info)

    def test_generate_random_query_no_api_key(self):
        """Test that generate_random_query raises error when no API key exists"""
        schema_info = {"tables": []}

        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="No LLM API key found"):
                generate_random_query(schema_info)

    def test_generate_validated_query_multiple_rows_returned(self):
        """Test that queries returning multiple rows are accepted"""
        schema_info = {
            "tables": [
                {
                    "name": "employees",
                    "columns": [
                        {"name": "id", "type": "INTEGER"},
                        {"name": "name", "type": "TEXT"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # Setup mocks with multiple rows
                        mock_nl_query.return_value = "Show me all employees"
                        mock_sql.return_value = "SELECT * FROM employees"
                        mock_execute.return_value = {
                            'results': [
                                {'id': 1, 'name': 'Alice'},
                                {'id': 2, 'name': 'Bob'},
                                {'id': 3, 'name': 'Charlie'}
                            ],
                            'columns': ['id', 'name'],
                            'error': None
                        }

                        # Call function
                        result = generate_validated_random_query(schema_info)

                        # Should succeed with multiple rows
                        assert result == "Show me all employees"
                        mock_execute.assert_called_once()

    def test_generate_validated_query_respects_max_attempts_parameter(self):
        """Test that the max_attempts parameter is respected"""
        schema_info = {
            "tables": [
                {
                    "name": "test",
                    "columns": [
                        {"name": "id", "type": "INTEGER"}
                    ]
                }
            ]
        }

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_random_query_with_openai') as mock_nl_query:
                with patch('core.llm_processor.generate_sql') as mock_sql:
                    with patch('core.llm_processor.execute_sql_safely') as mock_execute:
                        # All attempts fail
                        mock_nl_query.return_value = "Query"
                        mock_sql.return_value = "SELECT * FROM test"
                        mock_execute.return_value = {
                            'results': [],
                            'columns': [],
                            'error': None
                        }

                        # Test with custom max_attempts
                        with pytest.raises(Exception, match="after 2 attempts"):
                            generate_validated_random_query(schema_info, max_attempts=2)

                        # Should only try twice
                        assert mock_nl_query.call_count == 2
