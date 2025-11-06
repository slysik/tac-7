import os
import json
from typing import Dict, Any, List
from openai import OpenAI
from anthropic import Anthropic
from core.data_models import QueryRequest
from core.sql_processor import execute_sql_safely

def generate_sql_with_openai(query_text: str, schema_info: Dict[str, Any]) -> str:
    """
    Generate SQL query using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Convert this natural language query to SQL: "{query_text}"

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQLite syntax
- Handle date/time queries appropriately (e.g., "last week" = date('now', '-7 days'))
- Be careful with column names and table names
- If the query is ambiguous, make reasonable assumptions
- For multi-table queries, use proper JOIN conditions to avoid Cartesian products
- Limit results to reasonable amounts (e.g., add LIMIT 100 for large result sets)
- When joining tables, use meaningful relationships between tables
- NEVER include SQL comments (-- or /* */) in the query

SQL Query:"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Convert natural language to SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=500
        )
        
        sql = response.choices[0].message.content.strip()
        
        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        raise Exception(f"Error generating SQL with OpenAI: {str(e)}")

def generate_sql_with_anthropic(query_text: str, schema_info: Dict[str, Any]) -> str:
    """
    Generate SQL query using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        client = Anthropic(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Convert this natural language query to SQL: "{query_text}"

Rules:
- Return ONLY the SQL query, no explanations
- Use proper SQLite syntax
- Handle date/time queries appropriately (e.g., "last week" = date('now', '-7 days'))
- Be careful with column names and table names
- If the query is ambiguous, make reasonable assumptions
- For multi-table queries, use proper JOIN conditions to avoid Cartesian products
- Limit results to reasonable amounts (e.g., add LIMIT 100 for large result sets)
- When joining tables, use meaningful relationships between tables
- NEVER include SQL comments (-- or /* */) in the query

SQL Query:"""
        
        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=500,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        sql = response.content[0].text.strip()
        
        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.startswith("```"):
            sql = sql[3:]
        if sql.endswith("```"):
            sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        raise Exception(f"Error generating SQL with Anthropic: {str(e)}")

def format_schema_for_prompt(schema_info: Dict[str, Any]) -> str:
    """
    Format database schema for LLM prompt
    """
    lines = []
    
    for table_name, table_info in schema_info.get('tables', {}).items():
        lines.append(f"Table: {table_name}")
        lines.append("Columns:")
        
        for col_name, col_type in table_info['columns'].items():
            lines.append(f"  - {col_name} ({col_type})")
        
        lines.append(f"Row count: {table_info['row_count']}")
        lines.append("")
    
    return "\n".join(lines)

def generate_random_query_with_openai(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language query that someone might ask about this data. 
The query should be:
- Contextually relevant to the table structures and columns
- Natural and conversational
- Maximum two sentences
- Something that would demonstrate the capability of natural language to SQL conversion
- Varied in complexity (sometimes simple, sometimes complex with JOINs or aggregations)
- Do NOT include any SQL syntax, comments, or special characters

Examples of good queries:
- "What are the top 5 products by revenue?"
- "Show me all customers who ordered in the last month."
- "Which employees have the highest average sales? List their names and departments."

Natural language query:"""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates interesting questions about data."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=100
        )
        
        query = response.choices[0].message.content.strip()
        return query
        
    except Exception as e:
        raise Exception(f"Error generating random query with OpenAI: {str(e)}")

def generate_random_query_with_anthropic(schema_info: Dict[str, Any]) -> str:
    """
    Generate a random natural language query using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        client = Anthropic(api_key=api_key)
        
        # Format schema for prompt
        schema_description = format_schema_for_prompt(schema_info)
        
        # Create prompt
        prompt = f"""Given the following database schema:

{schema_description}

Generate an interesting natural language query that someone might ask about this data. 
The query should be:
- Contextually relevant to the table structures and columns
- Natural and conversational
- Maximum two sentences
- Something that would demonstrate the capability of natural language to SQL conversion
- Varied in complexity (sometimes simple, sometimes complex with JOINs or aggregations)
- Do NOT include any SQL syntax, comments, or special characters

Examples of good queries:
- "What are the top 5 products by revenue?"
- "Show me all customers who ordered in the last month."
- "Which employees have the highest average sales? List their names and departments."

Natural language query:"""
        
        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=100,
            temperature=0.8,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        query = response.content[0].text.strip()
        return query
        
    except Exception as e:
        raise Exception(f"Error generating random query with Anthropic: {str(e)}")

def generate_validated_random_query(schema_info: Dict[str, Any], max_attempts: int = 5) -> str:
    """
    Generate a validated random natural language query that returns data.

    This function generates a random natural language query and validates that it
    produces at least one row of results. If the query returns no results, it will
    retry up to max_attempts times.

    Args:
        schema_info: Database schema information
        max_attempts: Maximum number of attempts to generate a valid query (default: 5)

    Returns:
        A natural language query string that is validated to return results

    Raises:
        Exception: If unable to generate a valid query after max_attempts
    """
    for attempt in range(max_attempts):
        try:
            # Generate a random natural language query
            nl_query = generate_random_query_with_openai(schema_info) if os.environ.get("OPENAI_API_KEY") \
                       else generate_random_query_with_anthropic(schema_info)

            # Convert natural language query to SQL
            request = QueryRequest(query=nl_query, llm_provider="openai")
            sql_query = generate_sql(request, schema_info)

            # Execute the SQL query to validate it returns results
            result = execute_sql_safely(sql_query)

            # Check if we got an error during execution
            if result.get('error'):
                # Skip this query and try again
                continue

            # Check if the query returned at least one row
            if result.get('results') and len(result['results']) > 0:
                # Success! Return the validated natural language query
                return nl_query

            # Query executed successfully but returned no results, try again

        except Exception as e:
            # Log the error and continue to next attempt
            # In production, you might want to log this:
            # logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            continue

    # If we get here, all attempts failed
    raise Exception(
        f"Unable to generate a query that returns results after {max_attempts} attempts. "
        "Please verify that the database tables contain data."
    )

def generate_random_query(schema_info: Dict[str, Any]) -> str:
    """
    Route to appropriate LLM provider for random query generation with validation.
    Ensures the generated query returns at least one row of data.
    Priority: 1) OpenAI API key exists, 2) Anthropic API key exists
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability
    if not openai_key and not anthropic_key:
        raise ValueError("No LLM API key found. Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY")

    # Generate and validate random query
    return generate_validated_random_query(schema_info)

def generate_sql(request: QueryRequest, schema_info: Dict[str, Any]) -> str:
    """
    Route to appropriate LLM provider based on API key availability and request preference.
    Priority: 1) OpenAI API key exists, 2) Anthropic API key exists, 3) request.llm_provider
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability first (OpenAI priority)
    if openai_key:
        return generate_sql_with_openai(request.query, schema_info)
    elif anthropic_key:
        return generate_sql_with_anthropic(request.query, schema_info)

    # Fall back to request preference if both keys available or neither available
    if request.llm_provider == "openai":
        return generate_sql_with_openai(request.query, schema_info)
    else:
        return generate_sql_with_anthropic(request.query, schema_info)

def generate_synthetic_data_with_openai(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate synthetic data using OpenAI API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        client = OpenAI(api_key=api_key)

        # Format schema for prompt
        schema_lines = []
        for col_name, col_type in schema_info.items():
            schema_lines.append(f"  - {col_name}: {col_type}")
        schema_description = "\n".join(schema_lines)

        # Format sample rows for prompt
        sample_json = json.dumps(sample_rows, indent=2)

        # Create prompt
        prompt = f"""Given the following table schema and sample data, generate 10 new realistic synthetic data rows.

Table: {table_name}

Schema:
{schema_description}

Sample Data (for pattern analysis):
{sample_json}

Your task:
1. Analyze the data types and formats for each column
2. Study the value ranges and distributions in the sample data
3. Identify relationships between columns (e.g., city/state consistency)
4. Recognize common patterns (email formats, phone numbers, addresses, dates, etc.)
5. Respect nullable vs required fields (use null where appropriate)
6. Generate exactly 10 new rows with realistic variety (avoid repetitive patterns like "User 1", "User 2")

IMPORTANT:
- Return ONLY a valid JSON array of 10 objects
- Each object must have the EXACT same keys as the schema
- Use realistic data that matches the patterns in the sample data
- Ensure variety in the generated data (different names, emails, values, etc.)
- For emails, use realistic domains like gmail.com, yahoo.com, outlook.com
- For phone numbers, use valid formats consistent with sample data
- For addresses, use real city/state/country combinations
- For dates, use realistic date formats consistent with sample data
- Do NOT include any explanations, markdown, or extra text - ONLY the JSON array

Example output format:
[
  {{"column1": "value1", "column2": "value2", ...}},
  {{"column1": "value3", "column2": "value4", ...}},
  ...
]"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=[
                {"role": "system", "content": "You are a data generation expert. Generate realistic synthetic data that matches patterns in sample data."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2000
        )

        result = response.choices[0].message.content.strip()

        # Clean up the result (remove markdown if present)
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()

        # Parse JSON
        generated_data = json.loads(result)

        # Validate that we got exactly 10 rows
        if not isinstance(generated_data, list):
            raise ValueError("Generated data is not a list")
        if len(generated_data) != 10:
            raise ValueError(f"Expected 10 rows, got {len(generated_data)}")

        # Validate that each row has the correct columns
        expected_columns = set(schema_info.keys())
        for i, row in enumerate(generated_data):
            row_columns = set(row.keys())
            if row_columns != expected_columns:
                raise ValueError(f"Row {i} has incorrect columns. Expected {expected_columns}, got {row_columns}")

        return generated_data

    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON from OpenAI: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating synthetic data with OpenAI: {str(e)}")

def generate_synthetic_data_with_anthropic(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate synthetic data using Anthropic API
    """
    try:
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        # Format schema for prompt
        schema_lines = []
        for col_name, col_type in schema_info.items():
            schema_lines.append(f"  - {col_name}: {col_type}")
        schema_description = "\n".join(schema_lines)

        # Format sample rows for prompt
        sample_json = json.dumps(sample_rows, indent=2)

        # Create prompt
        prompt = f"""Given the following table schema and sample data, generate 10 new realistic synthetic data rows.

Table: {table_name}

Schema:
{schema_description}

Sample Data (for pattern analysis):
{sample_json}

Your task:
1. Analyze the data types and formats for each column
2. Study the value ranges and distributions in the sample data
3. Identify relationships between columns (e.g., city/state consistency)
4. Recognize common patterns (email formats, phone numbers, addresses, dates, etc.)
5. Respect nullable vs required fields (use null where appropriate)
6. Generate exactly 10 new rows with realistic variety (avoid repetitive patterns like "User 1", "User 2")

IMPORTANT:
- Return ONLY a valid JSON array of 10 objects
- Each object must have the EXACT same keys as the schema
- Use realistic data that matches the patterns in the sample data
- Ensure variety in the generated data (different names, emails, values, etc.)
- For emails, use realistic domains like gmail.com, yahoo.com, outlook.com
- For phone numbers, use valid formats consistent with sample data
- For addresses, use real city/state/country combinations
- For dates, use realistic date formats consistent with sample data
- Do NOT include any explanations, markdown, or extra text - ONLY the JSON array

Example output format:
[
  {{"column1": "value1", "column2": "value2", ...}},
  {{"column1": "value3", "column2": "value4", ...}},
  ...
]"""

        # Call Anthropic API
        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=2000,
            temperature=0.8,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text.strip()

        # Clean up the result (remove markdown if present)
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()

        # Parse JSON
        generated_data = json.loads(result)

        # Validate that we got exactly 10 rows
        if not isinstance(generated_data, list):
            raise ValueError("Generated data is not a list")
        if len(generated_data) != 10:
            raise ValueError(f"Expected 10 rows, got {len(generated_data)}")

        # Validate that each row has the correct columns
        expected_columns = set(schema_info.keys())
        for i, row in enumerate(generated_data):
            row_columns = set(row.keys())
            if row_columns != expected_columns:
                raise ValueError(f"Row {i} has incorrect columns. Expected {expected_columns}, got {row_columns}")

        return generated_data

    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON from Anthropic: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating synthetic data with Anthropic: {str(e)}")

def generate_synthetic_data(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Route to appropriate LLM provider for synthetic data generation
    Priority: 1) OpenAI API key exists, 2) Anthropic API key exists
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

    # Check API key availability (OpenAI priority)
    if openai_key:
        return generate_synthetic_data_with_openai(table_name, schema_info, sample_rows)
    elif anthropic_key:
        return generate_synthetic_data_with_anthropic(table_name, schema_info, sample_rows)
    else:
        raise ValueError("No LLM API key found. Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY")