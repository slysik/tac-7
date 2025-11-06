# E2E Test: Snowflake Migration

Test that the application works end-to-end with Snowflake as the backend database.

## User Story

As a system architect
I want to verify the Snowflake migration is complete and functional
So that the application works identically with the new cloud database backend

## Test Steps

### Part 1: Application Start & Health Check

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Available Tables section
5. **Verify** health check endpoint returns OK status with Snowflake connection

### Part 2: File Upload to Snowflake

1. Click the "Upload Data" button
2. Upload a sample CSV file (e.g., test_users.csv with columns: id, name, email, age)
3. **Verify** the upload succeeds
4. **Verify** a success message appears showing the table name
5. **Verify** the table appears in the "Available Tables" section
6. Take a screenshot of the uploaded table info
7. **Verify** the table schema is displayed correctly
8. **Verify** sample data preview is shown

### Part 3: Natural Language Query Execution

1. Enter a natural language query: "Show me all users from the uploaded table"
2. Take a screenshot of the query input
3. Click the Query button
4. **Verify** the query executes successfully
5. **Verify** SQL translation is displayed (should contain SELECT statement with Snowflake syntax)
6. Take a screenshot of the SQL translation
7. **Verify** results table contains the expected data
8. Take a screenshot of the query results
9. **Verify** row count matches expected results

### Part 4: Generate Synthetic Data

1. Navigate to the table in Available Tables section
2. Click "Generate Data" button for the uploaded table
3. **Verify** data generation succeeds
4. **Verify** success message shows number of rows added
5. **Verify** new row count is greater than original
6. Re-query the table to see new data
7. Take a screenshot showing the increased row count

### Part 5: Insights Generation

1. Click on "Column Insights" for the uploaded table
2. **Verify** insights are generated for all columns
3. **Verify** insights show:
   - Column names and data types (Snowflake types like NUMBER, VARCHAR)
   - Unique value counts
   - Null counts
   - Min/Max/Avg for numeric columns
4. Take a screenshot of the column insights

### Part 6: Export Functionality

1. Click "Export Table" button for the uploaded table
2. **Verify** CSV file downloads successfully
3. **Verify** downloaded CSV contains all table data
4. Run a query and export query results
5. **Verify** query results CSV downloads successfully

### Part 7: Table Deletion

1. Click "Delete Table" button for the uploaded table
2. **Verify** confirmation dialog appears
3. Confirm deletion
4. **Verify** table is removed from "Available Tables" section
5. **Verify** table no longer exists in Snowflake database
6. Take a screenshot of the empty Available Tables section

### Part 8: Verify No SQLite References

1. Check application logs for any SQLite-related errors
2. **Verify** all database operations use Snowflake connections
3. **Verify** no "db/database.db" file references in logs
4. **Verify** all INFORMATION_SCHEMA queries work correctly

## Success Criteria

- Application starts without errors using Snowflake backend
- File upload creates tables in Snowflake successfully
- Table names are uppercase (Snowflake convention)
- Natural language queries execute against Snowflake tables
- SQL translation shows correct Snowflake syntax (double quotes for identifiers)
- Results display correctly with Snowflake data types
- Generate data inserts rows into Snowflake tables
- Column insights use Snowflake data types (NUMBER, VARCHAR, etc.)
- Export functionality works with Snowflake connections
- Table deletion removes tables from Snowflake
- No SQLite references or errors in logs
- All CRUD operations work identically to SQLite version
- At least 7 screenshots are taken documenting the workflow

## Expected Behavior Differences

- Table names are uppercase in Snowflake (e.g., TEST_USERS vs test_users)
- Data types are Snowflake types (NUMBER, VARCHAR) not SQLite types (INTEGER, TEXT)
- Identifiers use double quotes (") not square brackets ([])
- INFORMATION_SCHEMA queries instead of sqlite_master queries

## Rollback Plan

If the E2E test fails:
1. Check Snowflake credentials in .env file
2. Verify Snowflake connection in health check endpoint
3. Check application logs for connection errors
4. Verify all sqlite3 imports have been replaced
5. Confirm INFORMATION_SCHEMA queries are correct
6. Test with a simple manual query to Snowflake
