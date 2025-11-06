# Chore: Only create sample query that return data

## Metadata
issue_number: `23`
adw_id: `7b271c38`
issue_json: `{"number":23,"title":"Only create sample query that return data.","body":"chore - adw_sdlc_zte_iso - update \"generate sample query\" to only generate sample queries that return results. Add checker to run sample to check that 1 or more rows are returned from table"}`

## Chore Description
Update the sample query generation system (`/api/generate-random-query` endpoint) to ensure that generated queries always return at least one row of data. Currently, the LLM generates random natural language queries based on the database schema, but there's no validation that the generated SQL will actually return results.

This chore implements a validation loop that:
1. Generates a sample natural language query using the LLM
2. Converts it to SQL using the existing SQL generation pipeline
3. Executes the SQL query to check if it returns 1+ rows
4. If the query returns no results, regenerates and tries again (with a maximum retry limit)
5. Returns only queries that are verified to return data

This ensures that sample queries demonstrate the application's capabilities with real data results, improving the user experience.

## Relevant Files
Use these files to resolve the chore:

- **app/server/core/llm_processor.py** (lines 146-265)
  - Contains `generate_random_query_with_openai()` and `generate_random_query_with_anthropic()` functions
  - Contains the `generate_random_query()` router function that needs to be updated
  - This is where the validation logic will be added to ensure generated queries return results

- **app/server/core/sql_processor.py** (lines 9-59)
  - Contains `execute_sql_safely()` function that executes SQL queries and returns results
  - Will be used to validate that generated queries return at least 1 row
  - Provides the necessary interface to check query results

- **app/server/server.py** (lines 218-244)
  - Contains the `/api/generate-random-query` endpoint
  - Calls `generate_random_query()` from llm_processor
  - May need minor updates to handle the new validation loop logic

- **app/server/tests/test_data_generation.py**
  - Existing test file for LLM-based generation features
  - Will be extended with new tests for the sample query validation logic

### New Files
- **app/server/tests/test_sample_query_validation.py**
  - New test file to specifically test the sample query validation loop
  - Tests will verify that queries return results, retry logic works, and error handling is proper

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create new utility function for query validation
- Add a new function `generate_validated_random_query()` in `app/server/core/llm_processor.py`
- This function will implement the validation loop:
  - Generate a random natural language query using existing `generate_random_query_with_openai()` or `generate_random_query_with_anthropic()`
  - Convert the natural language query to SQL using existing `generate_sql()` function
  - Execute the SQL using `execute_sql_safely()` from sql_processor
  - Check if the results contain 1+ rows
  - If no results, retry up to a maximum of 5 attempts
  - If all attempts fail, raise an exception with a descriptive error message
  - Return the validated natural language query that produces results

### Step 2: Update the generate_random_query router function
- Modify the `generate_random_query()` function in `app/server/core/llm_processor.py` (line 250)
- Change it to call the new `generate_validated_random_query()` function instead of directly calling the provider-specific functions
- Keep the existing API key priority logic (OpenAI first, then Anthropic)
- Ensure backward compatibility with the existing function signature

### Step 3: Update imports in server.py
- In `app/server/server.py` (line 29), verify that imports are correct
- Ensure `generate_sql` is imported since it will be used by the validation logic
- No other changes should be needed in server.py since the endpoint just calls `generate_random_query()`

### Step 4: Add comprehensive tests for query validation
- Create `app/server/tests/test_sample_query_validation.py`
- Test cases to include:
  - Test that queries returning results pass validation
  - Test that queries returning no results trigger retry logic
  - Test that retry logic stops after maximum attempts
  - Test that the function returns a query that produces results
  - Test error handling when SQL generation fails
  - Test error handling when query execution fails
  - Test with both OpenAI and Anthropic providers (using mocks)
  - Test that the validation loop respects the 5-attempt limit

### Step 5: Update existing tests if needed
- Review `app/server/tests/test_data_generation.py` to see if any existing tests need updates
- Ensure that tests still pass with the new validation logic
- Add any additional test cases that make sense in the existing test file

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest tests/test_sample_query_validation.py -v` - Run new validation tests
- `cd app/server && uv run pytest tests/test_data_generation.py -v` - Verify existing tests still pass
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions

## Notes
- The validation should be implemented as a loop with a maximum retry limit (5 attempts recommended) to avoid infinite loops
- Consider adding telemetry/logging to track how many retries are needed on average
- The prompt for generating random queries might need refinement to encourage queries that are more likely to return results (e.g., "Generate a query that would return interesting insights from the data")
- Consider caching the schema information to avoid repeated database calls during retry attempts
- The error message when all retries fail should be informative and suggest checking if the tables have any data
- This change is backward compatible - the API endpoint signature remains the same, only the internal validation logic is added
