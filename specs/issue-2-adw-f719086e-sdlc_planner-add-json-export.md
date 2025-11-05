# Feature: Add JSON Export

## Metadata
issue_number: `2`
adw_id: `f719086e`
issue_json: `{"number":2,"title":"Add json export","body":"feature - adw_sdlc_iso - update to support table and query result 'json' export. Similar to our csv export but specifically built for json export. "}`

## Feature Description
This feature extends the existing export functionality to support JSON format for both database tables and query results. Users will be able to export their data in JSON format alongside the existing CSV export capability. The JSON export will follow the same user experience patterns as CSV export, with dedicated download buttons and endpoints, providing users with flexibility in choosing the most appropriate data format for their downstream applications.

## User Story
As a data analyst or developer
I want to export table data and query results as JSON files
So that I can easily integrate the data with web APIs, modern applications, and data processing pipelines that consume JSON

## Problem Statement
Currently, the application only supports CSV export for tables and query results. While CSV is excellent for spreadsheet applications and traditional data analysis tools, modern web applications, APIs, and JavaScript-based data processing pipelines often require JSON format. Users working with REST APIs, NoSQL databases, or web frontend frameworks need a native way to export data in JSON format without manual conversion from CSV.

## Solution Statement
Implement a parallel JSON export system that mirrors the existing CSV export infrastructure. This will include:
- Server-side JSON generation utilities using Python's built-in json module
- New API endpoints `/api/export/table/json` and `/api/export/query/json`
- Client-side download functionality for JSON files
- UI controls (download buttons) positioned alongside existing CSV export buttons
- Comprehensive test coverage matching the existing CSV export tests

## Relevant Files
Use these files to implement the feature:

**Backend Files (Server):**
- `app/server/core/export_utils.py` - Contains CSV export utilities (`generate_csv_from_data` and `generate_csv_from_table`). We'll add JSON export functions here following the same patterns: `generate_json_from_data()` and `generate_json_from_table()`
- `app/server/core/data_models.py` - Contains export request models (`ExportRequest` and `QueryExportRequest`). These models will be reused for JSON exports, no changes needed
- `app/server/server.py` - Contains CSV export endpoints at lines 312-364. We'll add parallel JSON export endpoints: `/api/export/table/json` and `/api/export/query/json`
- `app/server/tests/test_export_utils.py` - Contains comprehensive CSV export tests. We'll add parallel JSON export tests

**Frontend Files (Client):**
- `app/client/src/api/client.ts` - Contains `exportTable()` and `exportQueryResults()` methods at lines 86-140. We'll add `exportTableJSON()` and `exportQueryResultsJSON()` methods
- `app/client/src/main.ts` - Contains UI logic for CSV export buttons. We'll add JSON export buttons positioned next to CSV export buttons
- `app/client/src/style.css` - Contains styling for export buttons. We'll add styling for JSON export buttons to maintain visual consistency

**Documentation Files:**
- `app_docs/feature-490eb6b5-one-click-table-exports.md` - Documents the CSV export feature. We'll reference this as the pattern for JSON export implementation
- `README.md` - Main project documentation at lines 8, 91. We may need to update features list to mention JSON export

### New Files

- `.claude/commands/e2e/test_json_export_functionality.md` - E2E test suite for JSON export features, mirroring the structure of `test_export_functionality.md` but validating JSON-specific functionality

## Implementation Plan
### Phase 1: Foundation
Create the core JSON export utilities in the backend, following the exact same patterns as CSV export but outputting JSON format. This includes:
- Implementing `generate_json_from_data()` function that converts data dictionaries and columns into formatted JSON
- Implementing `generate_json_from_table()` function that queries a database table and returns JSON
- Writing comprehensive unit tests covering all data types, edge cases, Unicode, and special characters

### Phase 2: Core Implementation
Add API endpoints and client-side functionality:
- Create `/api/export/table/json` endpoint that validates table names, generates JSON, and returns with appropriate headers
- Create `/api/export/query/json` endpoint that generates JSON from query results
- Add client API methods `exportTableJSON()` and `exportQueryResultsJSON()` with blob download handling
- Implement UI controls with JSON download buttons positioned logically near existing CSV export buttons

### Phase 3: Integration
Integrate JSON export into the existing UI workflow and validate end-to-end:
- Add JSON download buttons to the Available Tables section
- Add JSON download buttons to the Query Results section
- Style buttons consistently with existing UI patterns
- Create comprehensive E2E tests to validate the complete user workflow
- Validate all export operations work correctly with zero regressions to existing CSV functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create JSON Export Utility Functions

- Add `generate_json_from_data(data: List[Dict], columns: List[str]) -> bytes` function to `app/server/core/export_utils.py`
  - Function should accept data as list of dictionaries and columns as list of strings
  - Return formatted JSON with proper indentation (2 spaces) encoded as UTF-8 bytes
  - Handle empty data gracefully (return empty array as bytes)
  - Handle missing columns by auto-detecting from data keys if columns list is empty
- Add `generate_json_from_table(conn: sqlite3.Connection, table_name: str) -> bytes` function
  - Function should query the database table and return all rows as JSON
  - Raise `ValueError` if table doesn't exist
  - Use parameterized queries for security
  - Return formatted JSON with proper indentation encoded as UTF-8 bytes

### 2. Create Comprehensive Unit Tests for JSON Export

- Add JSON export tests to `app/server/tests/test_export_utils.py`
  - Test `test_generate_json_from_data_empty()` - validates empty data returns `b"[]"`
  - Test `test_generate_json_from_data_with_columns_no_data()` - validates columns with no data returns empty array
  - Test `test_generate_json_from_data_with_data()` - validates JSON generation with actual data
  - Test `test_generate_json_from_data_auto_columns()` - validates automatic column detection from data keys
  - Test `test_generate_json_from_data_various_types()` - validates integers, floats, strings, booleans, nulls
  - Test `test_generate_json_from_data_special_characters()` - validates commas, quotes, newlines, tabs
  - Test `test_generate_json_from_data_unicode()` - validates Unicode characters and emojis (测试, 😀🎉, Café)
  - Test `test_generate_json_from_table_nonexistent()` - validates ValueError for non-existent table
  - Test `test_generate_json_from_table_empty()` - validates empty array for empty table
  - Test `test_generate_json_from_table_with_data()` - validates JSON generation from populated table
  - Test `test_generate_json_from_table_special_name()` - validates tables with special characters in name
- Run tests to ensure all pass: `cd app/server && uv run pytest tests/test_export_utils.py -v`

### 3. Add JSON Export API Endpoints

- Add `/api/export/table/json` endpoint to `app/server/server.py` (after line 344)
  - Accept `ExportRequest` model (reuse existing model)
  - Validate table name using `validate_identifier()`
  - Check table exists using `check_table_exists()`
  - Generate JSON using `generate_json_from_table()`
  - Return `Response` with `media_type="application/json"` and `Content-Disposition` header with filename `{table_name}_export.json`
  - Handle errors with proper logging and HTTPException
- Add `/api/export/query/json` endpoint to `app/server/server.py` (after the table JSON endpoint)
  - Accept `QueryExportRequest` model (reuse existing model)
  - Generate JSON using `generate_json_from_data()`
  - Return `Response` with `media_type="application/json"` and `Content-Disposition` header with filename `query_results.json`
  - Handle errors with proper logging and HTTPException

### 4. Add Client API Methods for JSON Export

- Add `exportTableJSON(tableName: string): Promise<void>` method to `app/client/src/api/client.ts` (after line 114)
  - POST to `/export/table/json` endpoint with table name
  - Extract filename from `Content-Disposition` header, fallback to `{tableName}_export.json`
  - Download blob using same pattern as CSV export
  - Handle errors appropriately
- Add `exportQueryResultsJSON(data: any[], columns: string[]): Promise<void>` method (after the table JSON export method)
  - POST to `/export/query/json` endpoint with data and columns
  - Download blob with filename `query_results.json`
  - Handle errors appropriately

### 5. Add JSON Export Buttons to UI

- Update `app/client/src/main.ts` to add JSON export buttons for tables
  - Position JSON download button next to CSV download button in Available Tables section
  - Use similar icon/text pattern (e.g., "JSON ⬇" or just "JSON")
  - Wire up click handler to call `api.exportTableJSON(tableName)`
  - Add error handling with user-friendly error messages
- Add JSON export buttons for query results
  - Position JSON download button next to CSV download button in Query Results section
  - Wire up click handler to call `api.exportQueryResultsJSON(currentResults.data, currentResults.columns)`
  - Add error handling with user-friendly error messages

### 6. Style JSON Export Buttons

- Update `app/client/src/style.css` to add styling for JSON export buttons
  - Follow existing button styling patterns for consistency
  - Ensure proper spacing between CSV and JSON export buttons
  - Maintain visual hierarchy with other UI controls
  - Ensure buttons are clearly distinguishable from CSV export buttons

### 7. Create E2E Test for JSON Export

- Create `.claude/commands/e2e/test_json_export_functionality.md`
  - Follow the structure of `test_export_functionality.md` but validate JSON-specific functionality
  - Test Steps should include:
    1. Navigate to application and verify initial state
    2. Upload test CSV file and verify table appears
    3. Verify JSON download button appears for table
    4. Click JSON download button and verify JSON file downloads
    5. Verify downloaded JSON file contains valid JSON with correct data structure
    6. Execute query and verify results appear
    7. Verify JSON download button appears for query results
    8. Click JSON download button and verify JSON file downloads as `query_results.json`
    9. Verify downloaded JSON contains valid query results
    10. Execute empty result query and verify JSON download still works (empty array)
    11. Take screenshots at key steps
  - Success Criteria should validate JSON file validity, proper formatting, correct data, and appropriate filenames

### 8. Run All Validation Commands

- Execute all validation commands listed in the `Validation Commands` section below
- Ensure zero regressions in existing CSV export functionality
- Ensure all new JSON export functionality works as expected
- Fix any issues discovered during validation before completing the task

## Testing Strategy
### Unit Tests
- JSON generation from data dictionaries with various data types (integers, floats, strings, booleans, nulls)
- JSON generation from database tables including empty tables
- Edge cases: empty data, special characters, Unicode, large datasets
- Error handling: non-existent tables, invalid data
- JSON format validation: proper structure, indentation, encoding

### Edge Cases
- Empty tables and empty query results (should return `[]`)
- Tables with special characters in names (e.g., `special-table-name`)
- Data containing special JSON characters (quotes, backslashes, control characters)
- Unicode data (Chinese characters, emojis, accented characters)
- Null values in data (should become JSON `null`)
- Very large datasets (performance validation)
- Tables and queries with various SQLite data types (INTEGER, REAL, TEXT, BLOB, NULL)

## Acceptance Criteria
- JSON export functions generate valid, properly formatted JSON output
- All unit tests pass with 100% coverage for JSON export functions
- API endpoints `/api/export/table/json` and `/api/export/query/json` return valid JSON files with correct headers
- Client can successfully download JSON files for both tables and query results
- JSON export buttons appear in UI next to CSV export buttons with clear labeling
- Downloaded JSON files have appropriate names: `{table_name}_export.json` and `query_results.json`
- JSON format is properly indented (2 spaces) and human-readable
- Empty results produce valid JSON (empty array `[]`)
- All existing CSV export functionality continues to work without regression
- E2E test validates complete JSON export workflow end-to-end
- Security validation ensures table names are properly validated before export

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_json_export_functionality.md` test file to validate JSON export functionality works end-to-end
- `cd app/server && uv run pytest tests/test_export_utils.py -v` - Run all export utility tests including new JSON tests to validate zero regressions
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun run tsc --noEmit` - Run TypeScript compiler to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes
- JSON export leverages Python's built-in `json` module, requiring no new dependencies
- JSON format is widely supported by modern web applications, APIs, and data processing tools
- JSON export follows the exact same security patterns as CSV export (table name validation, SQL injection protection)
- JSON files are formatted with 2-space indentation for human readability
- The implementation maintains consistency with existing CSV export patterns for easier maintenance
- Future enhancements could include:
  - Configurable JSON formatting options (compact vs. pretty-printed)
  - Support for nested JSON structures from JOIN queries
  - JSON export with custom schemas or transformations
  - Batch export of multiple tables as a single JSON file with top-level keys
- Performance considerations: JSON serialization is generally fast for datasets up to 100,000 rows as specified in requirements
- JSON export will properly handle SQLite data types: INTEGER, REAL, TEXT, BLOB, NULL
