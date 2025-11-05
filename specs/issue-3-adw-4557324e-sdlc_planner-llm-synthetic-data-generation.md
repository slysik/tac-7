# Feature: LLM-Based Synthetic Data Generation for Tables

## Metadata
issue_number: `3`
adw_id: `4557324e`
issue_json: `{"number":3,"title":"Table Random Data Generation Based on Schema using LLMs","body":"Generate synthetic data rows based on existing table patterns and schema.\n\n/feature\n\nadw_sdlc_iso\n\nmodel_set_heavy\n\nimplement a random data generation feature that creates synthetic data rows based on existing table patterns. Add a new button to the left of the CSV export button in the Available Tables section that triggers LLM-based data generation. \n\nImplementation details:\n- Add \"Generate Data\" button with appropriate icon next to each table (left of CSV export) \n- When clicked, sample 10 random existing rows from the table\n- Send sampled data + table schema to LLM with prompt to understand data platforms\n- Generate 10 new synthetic rows that match the patterns and constraints\n- Insert generated rows into the table with proper validation \n- Show success notification with count of rows added\n\nThe LMM should analyze:\n- Datatypes and formats for each column\n- Value ranges and distributions\n- Relationships between columns \n- Common patterns (emails, phone numbers, addresses, etc.)\n- Nullable vs required fields.\n\nUpdate the UI to show a loading state generation and handle errors gracefully.  The feature should use the existing LLM processor module and respect SQL security constraints.   \n\nThis enhances testing and development by allowing users to quickly expand their datasets with realistic synthetic data. \n   "}`

## Feature Description
This feature enables users to automatically generate realistic synthetic data for their tables using LLM intelligence. When users click a "Generate Data" button next to any table in the Available Tables section, the system will analyze existing data patterns and use an LLM to generate 10 new rows that match the table's schema, data types, value distributions, and business logic patterns (like email formats, phone numbers, address structures, etc.). The generated data is validated and inserted into the table with proper security constraints, providing users with a quick way to expand their datasets for testing and development purposes.

## User Story
As a database user or developer
I want to automatically generate realistic synthetic data based on my existing table patterns
So that I can quickly expand my datasets for testing, development, and demonstration purposes without manually creating rows

## Problem Statement
Users often need to populate their tables with realistic test data for development, testing, or demonstration purposes. Manually creating test data is time-consuming, error-prone, and often results in unrealistic patterns. Current solutions either generate completely random data that doesn't match real-world patterns, or require users to write custom data generation scripts. There's a need for an intelligent data generation system that understands the existing data patterns, respects data types and constraints, and generates realistic synthetic data that matches the characteristics of the original dataset.

## Solution Statement
We will implement an LLM-powered synthetic data generation feature that analyzes existing table data and intelligently generates new rows matching the patterns. The solution adds a "Generate Data" button to each table in the Available Tables section. When clicked, the system samples 10 random existing rows, extracts the table schema, and sends this information to an LLM with a carefully crafted prompt that instructs it to analyze data types, value ranges, distributions, relationships between columns, and common patterns (emails, phone numbers, addresses, etc.). The LLM generates 10 new synthetic rows in JSON format, which are then validated against the SQL security constraints and inserted into the table. The UI shows a loading state during generation and displays a success notification with the count of rows added. This leverages the existing LLM processor module (which already supports both OpenAI and Anthropic) and respects all SQL security constraints to ensure safe data insertion.

## Relevant Files
Use these files to implement the feature:

- `app/server/core/llm_processor.py` - Contains the existing LLM integration for OpenAI and Anthropic APIs. We'll add a new function `generate_synthetic_data()` that takes table schema and sample rows, sends a prompt to the LLM, and returns generated data as structured JSON.

- `app/server/core/sql_security.py` - Contains SQL security utilities including identifier validation, safe query execution, and SQL injection protection. We'll use `validate_identifier()`, `execute_query_safely()`, and `check_table_exists()` to ensure secure data insertion.

- `app/server/core/data_models.py` - Contains Pydantic models for API requests/responses. We'll add new models: `GenerateDataRequest` (with table_name), `GenerateDataResponse` (with rows_added, new_row_count, error), and potentially a `SyntheticRow` model for structured data validation.

- `app/server/server.py` - The FastAPI application with all API endpoints. We'll add a new endpoint `POST /api/generate-data` that accepts a table name, validates it, samples existing rows, calls the LLM processor, validates the generated data, and inserts it into the table.

- `app/client/src/main.ts` - The frontend TypeScript file that handles UI interactions and API calls. We'll modify the `displayTables()` function to add a "Generate Data" button before the CSV export button, and create a new function `handleGenerateData()` to manage the button click, show loading state, call the API, and display success/error notifications.

- `app/client/src/api/client.ts` - The API client module that wraps fetch calls to the backend. We'll add a new method `generateTableData(tableName: string)` that makes a POST request to `/api/generate-data`.

- `app/client/src/types.d.ts` - TypeScript type definitions for API responses. We'll add the `GenerateDataResponse` interface matching the backend Pydantic model.

- `app/client/src/style.css` - Contains CSS styles for the application. We'll add styles for the "Generate Data" button (`.generate-data-button`) to match the existing button styles and ensure proper spacing between buttons.

- `README.md` - Project documentation. We'll update the API Endpoints section to document the new `/api/generate-data` endpoint and add the feature to the Features list.

- `.claude/commands/conditional_docs.md` - Conditional documentation guide. Since we're working with LLM model configurations and the llm_processor module, we should reference `app_docs/feature-4c768184-model-upgrades.md` to understand the existing LLM patterns.

### New Files

- `app/server/tests/test_data_generation.py` - Unit tests for the synthetic data generation functionality including: testing the LLM prompt construction, validating generated data structure, testing data insertion with various table schemas, edge cases (empty tables, tables with single row, tables with NULL values), security validation (SQL injection attempts in generated data), and error handling (LLM API failures, invalid JSON responses, schema mismatches).

- `.claude/commands/e2e/test_synthetic_data_generation.md` - E2E test file that validates the complete data generation workflow: upload sample data, verify "Generate Data" button appears, click the button, verify loading state, wait for completion, verify success notification shows "10 rows added", query the table to confirm new data exists, verify the data matches expected patterns and types, and take screenshots at each step to prove the feature works correctly.

## Implementation Plan

### Phase 1: Foundation
First, we'll extend the core server infrastructure to support synthetic data generation. This includes creating new Pydantic models for the API request/response, adding a new function to the LLM processor module that constructs an intelligent prompt for data generation, and implementing helper functions to sample existing table data safely. We'll ensure all SQL operations use the existing security utilities to prevent injection attacks. This phase establishes the foundation without touching the API endpoints or UI.

### Phase 2: Core Implementation
Next, we'll implement the main data generation logic. This includes creating the new API endpoint in server.py that orchestrates the entire flow: validating the table name, checking the table has sufficient data (at least 1 row), sampling 10 random existing rows, extracting the table schema, calling the LLM processor to generate synthetic data, parsing and validating the LLM's JSON response, constructing safe INSERT statements using parameterized queries, and handling errors at each step. We'll write comprehensive unit tests to validate each component works correctly with various table schemas and edge cases.

### Phase 3: Integration
Finally, we'll integrate the feature into the frontend UI. We'll add the "Generate Data" button to the table display with appropriate styling and positioning (to the left of the CSV export button), implement the button click handler with loading state management, add the API client method to call the backend, display success notifications showing the number of rows added, handle errors gracefully with user-friendly messages, and ensure the table row count updates after generation. We'll create an E2E test file to validate the complete user workflow from button click to data insertion, capturing screenshots at each step to prove the feature works as expected.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Read Conditional Documentation
- Read `.claude/commands/conditional_docs.md` to check if additional documentation is needed
- Read `app_docs/feature-4c768184-model-upgrades.md` to understand the existing LLM processor patterns and model configurations

### Task 2: Add Pydantic Models for Data Generation API
- Open `app/server/core/data_models.py`
- Add `GenerateDataRequest` model with `table_name: str` field
- Add `GenerateDataResponse` model with fields: `rows_added: int`, `new_row_count: int`, `table_name: str`, `error: Optional[str] = None`
- Ensure models follow the existing pattern with proper Field descriptions and type hints

### Task 3: Implement LLM Synthetic Data Generation Function
- Open `app/server/core/llm_processor.py`
- Add function `generate_synthetic_data_with_openai(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]`
- Add function `generate_synthetic_data_with_anthropic(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]`
- Add router function `generate_synthetic_data(table_name: str, schema_info: Dict[str, Any], sample_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]` that follows the same provider priority pattern as `generate_sql()`
- Construct intelligent prompts that instruct the LLM to:
  - Analyze the table schema (column names, data types, constraints)
  - Study the sample rows to understand value patterns, ranges, and distributions
  - Identify relationships between columns (e.g., city/state/country consistency)
  - Recognize common patterns like email formats, phone numbers, addresses, dates
  - Respect nullable vs required fields
  - Generate exactly 10 new rows as a JSON array of objects
  - Ensure realistic variety (avoid repetitive patterns)
- Parse the LLM response to extract JSON array
- Validate that the response contains exactly 10 rows with the correct column structure
- Handle errors (API failures, invalid JSON, schema mismatches)
- Write unit tests in `app/server/tests/test_llm_processor.py` for the new functions

### Task 4: Implement API Endpoint for Data Generation
- Open `app/server/server.py`
- Import the new models and LLM function
- Add endpoint `@app.post("/api/generate-data", response_model=GenerateDataResponse)`
- Implement the endpoint logic:
  1. Validate table_name using `validate_identifier()`
  2. Connect to database and check table exists using `check_table_exists()`
  3. Query current row count
  4. Check table has at least 1 existing row (return error if empty)
  5. Sample 10 random rows using `SELECT * FROM {table} ORDER BY RANDOM() LIMIT 10`
  6. Get table schema using existing `get_database_schema()` function
  7. Call `generate_synthetic_data()` from llm_processor
  8. For each generated row, construct INSERT statement using `execute_query_safely()` with parameterized queries
  9. Commit all insertions
  10. Query new row count
  11. Return GenerateDataResponse with rows_added and new_row_count
- Handle all errors with proper logging and user-friendly error messages
- Close database connections properly in finally blocks

### Task 5: Create Unit Tests for Data Generation
- Create file `app/server/tests/test_data_generation.py`
- Write test cases:
  - `test_generate_synthetic_data_openai()` - Mocks OpenAI API and verifies correct prompt construction
  - `test_generate_synthetic_data_anthropic()` - Mocks Anthropic API and verifies correct prompt construction
  - `test_generate_data_endpoint_success()` - Tests the full endpoint with mocked LLM responses
  - `test_generate_data_empty_table()` - Verifies error when table has 0 rows
  - `test_generate_data_table_not_exists()` - Verifies 404 error for non-existent table
  - `test_generate_data_invalid_table_name()` - Tests SQL security validation
  - `test_generate_data_llm_invalid_json()` - Handles cases where LLM returns malformed JSON
  - `test_generate_data_schema_mismatch()` - Handles cases where LLM returns wrong columns
  - `test_generate_data_sql_injection_attempt()` - Ensures security module blocks injection in generated data
- Run tests: `cd app/server && uv run pytest tests/test_data_generation.py -v`

### Task 6: Add Frontend API Client Method
- Open `app/client/src/api/client.ts`
- Add method to the `api` object:
```typescript
async generateTableData(tableName: string): Promise<GenerateDataResponse> {
  return apiRequest<GenerateDataResponse>('/generate-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ table_name: tableName })
  });
}
```

### Task 7: Add TypeScript Type Definitions
- Open `app/client/src/types.d.ts`
- Add interface:
```typescript
interface GenerateDataResponse {
  rows_added: number;
  new_row_count: number;
  table_name: string;
  error?: string;
}
```

### Task 8: Add "Generate Data" Button to UI
- Open `app/client/src/main.ts`
- Locate the `displayTables()` function
- Find where the CSV export button is created (around line 338-348)
- Before the export button creation, add code to create the "Generate Data" button:
```typescript
// Create generate data button
const generateButton = document.createElement('button');
generateButton.className = 'generate-data-button';
generateButton.innerHTML = '⚡ Generate';
generateButton.title = 'Generate synthetic data using AI';
generateButton.onclick = async () => {
  await handleGenerateData(table.name);
};
```
- Add the generateButton to buttonsContainer before the exportButton
- Implement `handleGenerateData()` function:
  1. Disable the button and show loading state (spinner)
  2. Call `api.generateTableData(tableName)`
  3. If successful, show success notification with rows added count
  4. Reload the database schema to update table row counts
  5. Re-enable the button
  6. Handle errors with user-friendly error messages

### Task 9: Add CSS Styles for Generate Data Button
- Open `app/client/src/style.css`
- Add styles for `.generate-data-button` matching the existing button pattern
- Ensure proper spacing and hover effects
- Add loading spinner styles if needed (may already exist)

### Task 10: Update Documentation
- Open `README.md`
- Add "🤖 LLM-based synthetic data generation" to the Features list
- Add `POST /api/generate-data` to the API Endpoints section with description
- Update the Usage section to mention the Generate Data button functionality

### Task 11: Create E2E Test File
- Create file `.claude/commands/e2e/test_synthetic_data_generation.md`
- Follow the pattern from `.claude/commands/e2e/test_basic_query.md`
- Include test steps:
  1. Navigate to application URL
  2. Take screenshot of initial state
  3. Click "Upload Data" and upload sample users.json
  4. Verify table appears with row count
  5. Take screenshot of table with Generate Data button
  6. Note the initial row count
  7. Click the "Generate Data" button (⚡ Generate)
  8. Verify loading state appears (button disabled, spinner visible)
  9. Wait for completion (up to 30 seconds for LLM response)
  10. Verify success notification appears with "10 rows added"
  11. Take screenshot of success notification
  12. Verify table row count increased by 10
  13. Query the table to see the new synthetic data: "Show me all users"
  14. Verify results contain realistic patterns (valid emails, names, etc.)
  15. Take screenshot of query results showing synthetic data
- Define success criteria: button appears, loading state works, data generation succeeds, notification shows correct count, data matches schema and patterns

### Task 12: Run All Tests to Validate Implementation
- Execute the validation commands listed in the Validation Commands section
- Ensure zero test failures and zero regressions
- Fix any issues discovered during testing

## Testing Strategy

### Unit Tests
1. **LLM Prompt Construction Tests**: Verify that prompts sent to OpenAI and Anthropic contain correct schema information, sample rows, and clear instructions for data generation
2. **Data Parsing Tests**: Validate parsing of LLM JSON responses, handling of malformed JSON, and validation of generated data structure
3. **Security Tests**: Ensure SQL injection attempts in table names are blocked, validate that parameterized queries are used for insertions, test that generated data with malicious content is sanitized
4. **Endpoint Tests**: Mock LLM responses and test the full API endpoint flow including error handling
5. **Empty Table Tests**: Verify appropriate error messages when attempting to generate data for tables with 0 rows
6. **Schema Validation Tests**: Ensure generated data columns match the table schema exactly

### Edge Cases
1. **Empty Tables**: Table with 0 rows should return a clear error message: "Cannot generate data for empty table. Please add at least one row first."
2. **Single Row Tables**: Table with exactly 1 row should still work, using that single row as the pattern
3. **Tables with NULL Values**: Generated data should respect nullable columns and include appropriate NULL values where observed in samples
4. **Tables with Special Characters**: Table names or column names with underscores or spaces should be properly escaped and validated
5. **Large Sample Sizes**: If table has fewer than 10 rows, sample all available rows instead of failing
6. **Complex Data Types**: Test with various SQLite types (INTEGER, REAL, TEXT, BLOB, DATE/TIME strings)
7. **LLM Failures**: Handle cases where LLM API is unavailable, returns 500 errors, or exceeds rate limits
8. **Invalid LLM Responses**: Handle cases where LLM returns valid JSON but with wrong schema (extra columns, missing columns, wrong types)
9. **Concurrent Requests**: Test behavior when multiple users generate data for the same table simultaneously
10. **Very Large Tables**: Ensure random sampling works efficiently even for tables with millions of rows

## Acceptance Criteria
1. "Generate Data" button (⚡ Generate) appears to the left of the CSV export button for every table in the Available Tables section
2. Button is styled consistently with existing UI patterns and has appropriate hover effects
3. Clicking the button disables it and shows a loading spinner while generation is in progress
4. The system samples up to 10 random existing rows from the table (or all rows if fewer than 10)
5. The table schema is correctly extracted and sent to the LLM
6. The LLM generates exactly 10 new synthetic rows that match the table schema
7. Generated data respects data types, value patterns, and relationships observed in sample data
8. Common patterns (emails, phone numbers, addresses, dates) are recognized and replicated realistically
9. All SQL operations use parameterized queries and the security module to prevent injection attacks
10. Generated rows are successfully inserted into the table
11. A success notification appears showing "Generated 10 rows for table '[table_name]'. New total: [new_count] rows."
12. The table row count in the UI updates automatically after generation
13. If an error occurs (empty table, LLM failure, etc.), a clear error message is displayed to the user
14. The feature works with both OpenAI and Anthropic LLM providers following the existing priority pattern
15. All existing functionality continues to work without regression (uploads, queries, exports, table deletion)
16. Unit tests achieve >90% code coverage for new functions
17. E2E test successfully validates the complete workflow from button click to data insertion

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the E2E test file `.claude/commands/e2e/test_synthetic_data_generation.md` to validate the data generation feature works end-to-end with screenshots proving functionality.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/test_data_generation.py -v` - Run specific data generation tests with verbose output
- `cd app/server && uv run pytest tests/test_sql_injection.py -v` - Ensure SQL security tests still pass with new endpoint
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript compilation to validate type safety
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### LLM Model Selection
The feature will use the existing LLM provider priority pattern from `llm_processor.py`: OpenAI first (if API key exists), then Anthropic. This ensures consistency with the rest of the application and allows users to use their preferred provider.

### Prompt Engineering Considerations
The prompt sent to the LLM should be carefully crafted to:
- Provide clear examples of the expected JSON output format
- Emphasize the importance of matching the exact schema (column names and types)
- Encourage realistic variety (avoiding repetitive patterns like "User 1", "User 2", etc.)
- Request realistic data patterns for common field types (emails ending in common domains, phone numbers with valid formats, addresses with real city/state combinations)
- Specify that NULL values should be used appropriately for nullable columns
- Request that relationships between fields are maintained (e.g., if city is "New York", state should be "NY")

### Performance Considerations
- LLM API calls typically take 2-10 seconds depending on the provider and model
- The UI should show a clear loading state during this time
- Consider adding a timeout (e.g., 30 seconds) to prevent indefinite waiting
- Sampling 10 rows from large tables should use `ORDER BY RANDOM() LIMIT 10` for efficiency

### Future Enhancements (Out of Scope)
- Allow users to specify the number of rows to generate (currently fixed at 10)
- Add a "Generate More" quick action to repeat generation without clicking the button again
- Implement batch generation for multiple tables at once
- Add a preview modal showing generated data before insertion with accept/reject options
- Store generation history and allow users to undo generations
- Add configuration options for generation parameters (temperature, creativity level)
- Support for generating data that references other tables (foreign key relationships)
