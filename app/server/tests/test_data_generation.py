import pytest
import json
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_synthetic_data_with_openai,
    generate_synthetic_data_with_anthropic,
    generate_synthetic_data
)


class TestSyntheticDataGeneration:
    """Tests for synthetic data generation functionality"""

    def test_generate_synthetic_data_openai(self):
        """Test OpenAI synthetic data generation with mocked API"""
        # Mock data
        table_name = "users"
        schema_info = {
            "id": "INTEGER",
            "name": "TEXT",
            "email": "TEXT",
            "age": "INTEGER"
        }
        sample_rows = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 30},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 25}
        ]

        # Mock LLM response
        mock_response = [
            {"id": 3, "name": "Bob Wilson", "email": "bob@gmail.com", "age": 35},
            {"id": 4, "name": "Alice Brown", "email": "alice@yahoo.com", "age": 28},
            {"id": 5, "name": "Charlie Davis", "email": "charlie@outlook.com", "age": 42},
            {"id": 6, "name": "Diana Evans", "email": "diana@gmail.com", "age": 31},
            {"id": 7, "name": "Ethan Foster", "email": "ethan@yahoo.com", "age": 27},
            {"id": 8, "name": "Fiona Green", "email": "fiona@outlook.com", "age": 33},
            {"id": 9, "name": "George Harris", "email": "george@gmail.com", "age": 29},
            {"id": 10, "name": "Hannah Irving", "email": "hannah@yahoo.com", "age": 36},
            {"id": 11, "name": "Ian Johnson", "email": "ian@outlook.com", "age": 24},
            {"id": 12, "name": "Julia King", "email": "julia@gmail.com", "age": 38}
        ]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                # Mock the API response
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                mock_completion.choices[0].message.content = json.dumps(mock_response)
                mock_client.chat.completions.create.return_value = mock_completion

                # Call the function
                result = generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

                # Assertions
                assert len(result) == 10
                assert all(isinstance(row, dict) for row in result)
                assert all(set(row.keys()) == set(schema_info.keys()) for row in result)

                # Verify API was called
                mock_client.chat.completions.create.assert_called_once()
                call_args = mock_client.chat.completions.create.call_args
                assert call_args[1]['model'] == 'o4-mini-2025-04-16'
                assert call_args[1]['max_completion_tokens'] == 2000

    def test_generate_synthetic_data_anthropic(self):
        """Test Anthropic synthetic data generation with mocked API"""
        # Mock data
        table_name = "products"
        schema_info = {
            "id": "INTEGER",
            "name": "TEXT",
            "price": "REAL",
            "category": "TEXT"
        }
        sample_rows = [
            {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
            {"id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics"}
        ]

        # Mock LLM response
        mock_response = [
            {"id": 3, "name": "Keyboard", "price": 79.99, "category": "Electronics"},
            {"id": 4, "name": "Monitor", "price": 299.99, "category": "Electronics"},
            {"id": 5, "name": "Desk Chair", "price": 199.99, "category": "Furniture"},
            {"id": 6, "name": "Webcam", "price": 89.99, "category": "Electronics"},
            {"id": 7, "name": "Headphones", "price": 149.99, "category": "Electronics"},
            {"id": 8, "name": "Desk Lamp", "price": 39.99, "category": "Furniture"},
            {"id": 9, "name": "USB Cable", "price": 9.99, "category": "Electronics"},
            {"id": 10, "name": "Notebook", "price": 4.99, "category": "Stationery"},
            {"id": 11, "name": "Pen Set", "price": 14.99, "category": "Stationery"},
            {"id": 12, "name": "Mouse Pad", "price": 12.99, "category": "Electronics"}
        ]

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            with patch('core.llm_processor.Anthropic') as mock_anthropic:
                # Mock the API response
                mock_client = MagicMock()
                mock_anthropic.return_value = mock_client
                mock_message = MagicMock()
                mock_message.content[0].text = json.dumps(mock_response)
                mock_client.messages.create.return_value = mock_message

                # Call the function
                result = generate_synthetic_data_with_anthropic(table_name, schema_info, sample_rows)

                # Assertions
                assert len(result) == 10
                assert all(isinstance(row, dict) for row in result)
                assert all(set(row.keys()) == set(schema_info.keys()) for row in result)

                # Verify API was called
                mock_client.messages.create.assert_called_once()
                call_args = mock_client.messages.create.call_args
                assert call_args[1]['model'] == 'claude-sonnet-4-0'
                assert call_args[1]['temperature'] == 0.8

    def test_generate_synthetic_data_router_openai_priority(self):
        """Test that generate_synthetic_data routes to OpenAI when API key exists"""
        table_name = "test_table"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.generate_synthetic_data_with_openai') as mock_openai:
                mock_openai.return_value = [{"id": 2, "name": "Generated"}] * 10

                result = generate_synthetic_data(table_name, schema_info, sample_rows)

                mock_openai.assert_called_once_with(table_name, schema_info, sample_rows)
                assert len(result) == 10

    def test_generate_synthetic_data_router_anthropic_fallback(self):
        """Test that generate_synthetic_data routes to Anthropic when only Anthropic key exists"""
        table_name = "test_table"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}, clear=True):
            with patch('core.llm_processor.generate_synthetic_data_with_anthropic') as mock_anthropic:
                mock_anthropic.return_value = [{"id": 2, "name": "Generated"}] * 10

                result = generate_synthetic_data(table_name, schema_info, sample_rows)

                mock_anthropic.assert_called_once_with(table_name, schema_info, sample_rows)
                assert len(result) == 10

    def test_generate_synthetic_data_no_api_key(self):
        """Test that generate_synthetic_data raises error when no API key exists"""
        table_name = "test_table"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="No LLM API key found"):
                generate_synthetic_data(table_name, schema_info, sample_rows)

    def test_generate_synthetic_data_invalid_json(self):
        """Test handling of invalid JSON response from LLM"""
        table_name = "users"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                mock_completion.choices[0].message.content = "This is not valid JSON"
                mock_client.chat.completions.create.return_value = mock_completion

                with pytest.raises(Exception, match="Error parsing JSON from OpenAI"):
                    generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

    def test_generate_synthetic_data_wrong_row_count(self):
        """Test handling when LLM returns incorrect number of rows"""
        table_name = "users"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        # Mock response with only 5 rows instead of 10
        mock_response = [
            {"id": 2, "name": "User 2"},
            {"id": 3, "name": "User 3"},
            {"id": 4, "name": "User 4"},
            {"id": 5, "name": "User 5"},
            {"id": 6, "name": "User 6"}
        ]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                mock_completion.choices[0].message.content = json.dumps(mock_response)
                mock_client.chat.completions.create.return_value = mock_completion

                with pytest.raises(Exception, match="Expected 10 rows, got 5"):
                    generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

    def test_generate_synthetic_data_schema_mismatch(self):
        """Test handling when LLM returns rows with incorrect schema"""
        table_name = "users"
        schema_info = {"id": "INTEGER", "name": "TEXT", "email": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test", "email": "test@example.com"}]

        # Mock response missing the email column
        mock_response = [
            {"id": 2, "name": "User 2"},
            {"id": 3, "name": "User 3"},
            {"id": 4, "name": "User 4"},
            {"id": 5, "name": "User 5"},
            {"id": 6, "name": "User 6"},
            {"id": 7, "name": "User 7"},
            {"id": 8, "name": "User 8"},
            {"id": 9, "name": "User 9"},
            {"id": 10, "name": "User 10"},
            {"id": 11, "name": "User 11"}
        ]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                mock_completion.choices[0].message.content = json.dumps(mock_response)
                mock_client.chat.completions.create.return_value = mock_completion

                with pytest.raises(Exception, match="Row 0 has incorrect columns"):
                    generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

    def test_generate_synthetic_data_with_markdown(self):
        """Test that markdown code blocks are properly stripped from LLM response"""
        table_name = "users"
        schema_info = {"id": "INTEGER", "name": "TEXT"}
        sample_rows = [{"id": 1, "name": "Test"}]

        mock_response = [{"id": i, "name": f"User {i}"} for i in range(2, 12)]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                # LLM response wrapped in markdown code block
                mock_completion.choices[0].message.content = f"```json\n{json.dumps(mock_response)}\n```"
                mock_client.chat.completions.create.return_value = mock_completion

                result = generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

                # Should successfully parse despite markdown
                assert len(result) == 10
                assert all(set(row.keys()) == set(schema_info.keys()) for row in result)

    def test_generate_synthetic_data_with_null_values(self):
        """Test that generated data can contain null values for nullable columns"""
        table_name = "users"
        schema_info = {"id": "INTEGER", "name": "TEXT", "age": "INTEGER"}
        sample_rows = [
            {"id": 1, "name": "Test User", "age": 30},
            {"id": 2, "name": "Another User", "age": None}  # Sample contains null
        ]

        mock_response = [
            {"id": 3, "name": "User 3", "age": 25},
            {"id": 4, "name": "User 4", "age": None},  # Allow null in generated data
            {"id": 5, "name": "User 5", "age": 35},
            {"id": 6, "name": "User 6", "age": 28},
            {"id": 7, "name": "User 7", "age": None},
            {"id": 8, "name": "User 8", "age": 42},
            {"id": 9, "name": "User 9", "age": 31},
            {"id": 10, "name": "User 10", "age": 27},
            {"id": 11, "name": "User 11", "age": None},
            {"id": 12, "name": "User 12", "age": 33}
        ]

        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            with patch('core.llm_processor.OpenAI') as mock_openai:
                mock_client = MagicMock()
                mock_openai.return_value = mock_client
                mock_completion = MagicMock()
                mock_completion.choices[0].message.content = json.dumps(mock_response)
                mock_client.chat.completions.create.return_value = mock_completion

                result = generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)

                # Verify null values are preserved
                assert len(result) == 10
                null_ages = [row for row in result if row['age'] is None]
                assert len(null_ages) > 0  # At least some null values should be present
