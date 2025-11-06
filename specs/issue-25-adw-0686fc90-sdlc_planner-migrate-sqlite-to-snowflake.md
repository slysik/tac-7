# Feature: Migrate Backend Database from SQLite to Snowflake

## Metadata
issue_number: `25`
adw_id: `0686fc90`
issue_json: `{"number":25,"title":"Change backed database from sqlite to snowflake","body":"feature  - adw_sdlc_zte_iso \n\nChange backed database from sqlite to snowflake. cred can be founder here: /Users/slysik/tac/tac-7/.env.snow. make sure all references and connections sqlite are updated to snowflake"}`

## Feature Description
Migrate the Natural Language SQL Interface application from using SQLite as the backend database to Snowflake, a cloud-based data warehouse platform. This migration will enable the application to leverage Snowflake's enterprise-grade features including scalability, concurrency, data sharing, and advanced analytics capabilities. All database connections, queries, and operations currently using SQLite will be updated to use Snowflake with credentials from `/Users/slysik/tac/tac-7/.env.snow`.

## User Story
As a system architect
I want to migrate the backend database from SQLite to Snowflake
So that the application can scale to handle enterprise workloads, support multiple concurrent users, and leverage cloud-native data warehousing capabilities

## Problem Statement
The current application uses SQLite, a file-based embedded database suitable for development and small-scale deployments. However, SQLite has limitations for production environments:
- Single-writer concurrency limitations
- No built-in user management or access control
- Limited to single-server deployments
- No native cloud integration
- Lacks advanced analytics and data sharing features

For enterprise use cases requiring multi-user access, scalability, and cloud-native features, a migration to Snowflake is necessary.

## Solution Statement
Replace all SQLite database connections and operations with Snowflake equivalents using the `snowflake-connector-python` library. This involves:
- Installing the Snowflake Python connector
- Creating a database configuration module to manage Snowflake connections
- Updating all database operations to use Snowflake-compatible SQL syntax
- Modifying data type mappings from SQLite to Snowflake
- Updating security utilities to work with Snowflake's identifier quoting conventions
- Ensuring all tests pass with the new backend
- Creating comprehensive E2E tests to validate the migration

## Relevant Files
Use these files to implement the feature:

- `app/server/core/sql_processor.py` - Contains SQLite database connection and query execution logic; needs update to use Snowflake connection
- `app/server/core/file_processor.py` - Handles CSV/JSON file uploads and table creation using SQLite; needs update for Snowflake
- `app/server/core/sql_security.py` - SQL security and identifier escaping using SQLite conventions; needs update for Snowflake's identifier quoting
- `app/server/core/insights.py` - Generates column insights using SQLite PRAGMA commands; needs update for Snowflake INFORMATION_SCHEMA queries
- `app/server/server.py` - FastAPI endpoints using SQLite connections; needs update to use Snowflake
- `app/server/pyproject.toml` - Python dependencies; needs to add `snowflake-connector-python`
- `app/server/.env.sample` - Environment variable template; needs Snowflake credential placeholders
- `app/server/tests/core/test_sql_processor.py` - Tests for SQL processor; needs update for Snowflake
- `app/server/tests/core/test_file_processor.py` - Tests for file processor; needs update for Snowflake
- `app/server/tests/test_sql_injection.py` - SQL injection security tests; needs verification with Snowflake
- `/Users/slysik/tac/tac-7/.env.snow` - Contains Snowflake credentials to be used for connection
- `README.md` - Project documentation; needs update to reflect Snowflake usage

### New Files

- `app/server/core/database.py` - New module to manage Snowflake connection pooling and configuration
- `app/server/tests/core/test_database.py` - Unit tests for the new database module
- `.claude/commands/e2e/test_snowflake_migration.md` - E2E test to validate Snowflake migration works end-to-end

## Implementation Plan

### Phase 1: Foundation
1. Install and configure the Snowflake connector library
2. Create a centralized database configuration module for Snowflake connection management
3. Update environment variable configuration to include Snowflake credentials
4. Establish connection patterns and best practices for Snowflake in the codebase

### Phase 2: Core Implementation
1. Update SQL security module to use Snowflake identifier quoting (double quotes instead of square brackets)
2. Migrate SQL processor to use Snowflake connections and syntax
3. Update file processor to create tables in Snowflake with proper data type mappings
4. Modify insights generation to use Snowflake INFORMATION_SCHEMA instead of SQLite PRAGMA commands
5. Update all API endpoints to use Snowflake connections

### Phase 3: Integration
1. Update all existing unit tests to work with Snowflake or mock Snowflake connections
2. Validate SQL injection protection still works with Snowflake
3. Create comprehensive E2E tests to validate the migration
4. Update documentation to reflect Snowflake configuration and setup
5. Verify all existing features work identically with Snowflake backend

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Snowflake Dependencies
- Add `snowflake-connector-python` to `app/server/pyproject.toml` dependencies using `uv add snowflake-connector-python`
- Sync dependencies with `uv sync --all-extras`

### Step 2: Create Database Configuration Module
- Create `app/server/core/database.py` with:
  - Snowflake connection factory function that reads credentials from environment variables
  - Connection pooling or connection management utilities
  - Helper functions for getting database connections
  - Configuration validation to ensure all required Snowflake credentials are present
- Use credentials structure from `/Users/slysik/tac/tac-7/.env.snow`: account, user, password, role, warehouse, database, schema

### Step 3: Update Environment Configuration
- Update `app/server/.env.sample` to include Snowflake credential placeholders:
  - `SNOWFLAKE_ACCOUNT`
  - `SNOWFLAKE_USER`
  - `SNOWFLAKE_PASSWORD`
  - `SNOWFLAKE_ROLE`
  - `SNOWFLAKE_WAREHOUSE`
  - `SNOWFLAKE_DATABASE`
  - `SNOWFLAKE_SCHEMA`
- Copy credentials from `/Users/slysik/tac/tac-7/.env.snow` to `app/server/.env` (if not already present)

### Step 4: Update SQL Security Module
- Modify `app/server/core/sql_security.py`:
  - Update `escape_identifier()` to use double quotes (`"identifier"`) instead of square brackets (`[identifier]`) for Snowflake compatibility
  - Ensure `validate_identifier()` works with Snowflake naming conventions
  - Update any SQLite-specific security checks to be Snowflake-compatible
  - Keep all existing security validations intact

### Step 5: Update SQL Processor Module
- Modify `app/server/core/sql_processor.py`:
  - Replace `sqlite3.connect("db/database.db")` with Snowflake connection from `core.database`
  - Update `execute_sql_safely()` to use Snowflake connector cursor
  - Modify `get_database_schema()` to use Snowflake INFORMATION_SCHEMA queries instead of `sqlite_master`
  - Update row factory pattern to work with Snowflake cursor results
  - Ensure all query executions use Snowflake-compatible SQL syntax

### Step 6: Update File Processor Module
- Modify `app/server/core/file_processor.py`:
  - Replace all `sqlite3.connect()` calls with Snowflake connections
  - Update data type mappings from pandas to Snowflake types (instead of SQLite types)
  - Modify `convert_csv_to_sqlite()` → `convert_csv_to_snowflake()` (or keep name but update implementation)
  - Modify `convert_json_to_sqlite()` → `convert_json_to_snowflake()`
  - Modify `convert_jsonl_to_sqlite()` → `convert_jsonl_to_snowflake()`
  - Update pandas `to_sql()` calls to work with Snowflake connection
  - Update PRAGMA queries to INFORMATION_SCHEMA queries for schema inspection

### Step 7: Update Insights Module
- Modify `app/server/core/insights.py`:
  - Replace `sqlite3.connect()` with Snowflake connection
  - Replace `PRAGMA table_info()` queries with Snowflake INFORMATION_SCHEMA queries:
    - `SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?`
  - Ensure all statistical queries work with Snowflake SQL dialect
  - Update NULL checks and aggregate functions if needed for Snowflake compatibility

### Step 8: Update FastAPI Server Endpoints
- Modify `app/server/server.py`:
  - Replace all `sqlite3.connect("db/database.db")` with Snowflake connections from `core.database`
  - Update health check endpoint to verify Snowflake connection instead of SQLite
  - Update schema retrieval to use Snowflake INFORMATION_SCHEMA
  - Ensure all endpoints properly close Snowflake connections
  - Update table deletion to use Snowflake DROP TABLE syntax

### Step 9: Create Unit Tests for Database Module
- Create `app/server/tests/core/test_database.py`:
  - Test connection factory creates valid Snowflake connections
  - Test credential validation
  - Test connection error handling
  - Use mocking for Snowflake connector to avoid requiring actual Snowflake instance in tests

### Step 10: Update Existing Unit Tests
- Update `app/server/tests/core/test_sql_processor.py`:
  - Mock Snowflake connections instead of SQLite
  - Update assertions for Snowflake response formats
  - Ensure tests validate Snowflake-specific behavior
- Update `app/server/tests/core/test_file_processor.py`:
  - Mock Snowflake connections
  - Update data type assertions for Snowflake types
  - Validate Snowflake table creation logic
- Update `app/server/tests/test_sql_injection.py`:
  - Verify security checks work with Snowflake identifier quoting
  - Test that Snowflake-specific injection patterns are blocked

### Step 11: Create E2E Test for Snowflake Migration
- Create `.claude/commands/e2e/test_snowflake_migration.md` following the pattern of `test_basic_query.md`
- Test should validate:
  - Application starts successfully with Snowflake backend
  - File upload creates tables in Snowflake
  - Natural language queries execute against Snowflake tables
  - Results are displayed correctly
  - All CRUD operations work (create table, query, generate data, delete table)
  - Screenshots demonstrate functionality

### Step 12: Update Documentation
- Update `README.md`:
  - Replace references to SQLite with Snowflake
  - Add Snowflake setup instructions
  - Update prerequisites to include Snowflake account
  - Document Snowflake credential configuration
  - Update architecture description to reflect cloud database
  - Remove SQLite-specific notes (e.g., "db/database.db" references)

### Step 13: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions and complete migration

## Testing Strategy

### Unit Tests
1. **Database Connection Tests** (`test_database.py`):
   - Test connection factory with valid credentials
   - Test connection factory with invalid credentials
   - Test connection pooling behavior
   - Test environment variable validation

2. **SQL Security Tests** (`test_sql_injection.py`):
   - Verify identifier escaping uses Snowflake double-quote syntax
   - Test SQL injection patterns are blocked with Snowflake
   - Validate parameterized queries work correctly
   - Test dangerous operation detection

3. **SQL Processor Tests** (`test_sql_processor.py`):
   - Test query execution with Snowflake connection
   - Test schema retrieval from Snowflake INFORMATION_SCHEMA
   - Test error handling with Snowflake-specific errors
   - Mock Snowflake connections to avoid live database dependency

4. **File Processor Tests** (`test_file_processor.py`):
   - Test CSV to Snowflake table conversion
   - Test JSON to Snowflake table conversion
   - Test JSONL to Snowflake table conversion
   - Verify data type mappings are correct for Snowflake
   - Mock Snowflake connections

### Edge Cases
1. **Connection Failures**:
   - Missing Snowflake credentials
   - Invalid credentials
   - Network timeouts
   - Warehouse suspended or unavailable

2. **Data Type Mismatches**:
   - SQLite INTEGER vs Snowflake NUMBER
   - SQLite TEXT vs Snowflake VARCHAR
   - Nested JSON structures in JSONL files
   - NULL handling differences

3. **Identifier Quoting**:
   - Reserved words as table names
   - Special characters in column names
   - Case sensitivity differences between SQLite and Snowflake

4. **Concurrency**:
   - Multiple simultaneous uploads
   - Concurrent queries on same table
   - Connection pool exhaustion

5. **Large Data Sets**:
   - CSV files exceeding memory limits
   - Very wide tables (many columns)
   - Tables with millions of rows

## Acceptance Criteria
- [ ] Snowflake connector library is installed and configured
- [ ] All SQLite connections replaced with Snowflake connections
- [ ] Database configuration module created with connection management
- [ ] Snowflake credentials loaded from environment variables (from .env.snow)
- [ ] All API endpoints work with Snowflake backend
- [ ] File uploads create tables in Snowflake successfully
- [ ] Natural language queries execute against Snowflake tables
- [ ] SQL security module uses Snowflake identifier quoting (double quotes)
- [ ] Insights generation uses Snowflake INFORMATION_SCHEMA
- [ ] All unit tests pass with Snowflake or mocked Snowflake connections
- [ ] E2E test validates complete Snowflake migration functionality
- [ ] No SQLite references remain in the codebase (except in comments/docs referencing the migration)
- [ ] Documentation updated to reflect Snowflake setup and configuration
- [ ] Application starts and runs without errors using Snowflake backend
- [ ] All existing features (upload, query, generate data, delete table, export) work identically

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_snowflake_migration.md` test file to validate the Snowflake migration works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- `grep -r "sqlite3" app/server --exclude-dir=__pycache__ --exclude="*.pyc"` - Verify no remaining sqlite3 imports except in migration notes
- `grep -r "db/database.db" app/server --exclude-dir=__pycache__` - Verify no hardcoded SQLite database paths remain
- `cd app/server && uv run python -c "import snowflake.connector; print('Snowflake connector installed successfully')"` - Verify Snowflake connector is installed

## Notes

### Snowflake Credentials Location
- Credentials are available at `/Users/slysik/tac/tac-7/.env.snow`
- Format:
  ```
  [snowflake]
  account = "DDGLEJK-VKA00124"
  user = "SLYSIK"
  password = "HighestAlign1!
  role = "ACCOUNTADMIN"
  warehouse = "FOO"
  database = "SNOWFLAKE_SAMPLE_DATA"
  schema = "TPCDS_SF10TCL"
  ```
- Convert to environment variables format for `app/server/.env`

### Key Differences: SQLite vs Snowflake

1. **Connection**:
   - SQLite: `sqlite3.connect("db/database.db")`
   - Snowflake: `snowflake.connector.connect(account=..., user=..., password=..., ...)`

2. **Identifier Quoting**:
   - SQLite: `[table_name]` or `"table_name"`
   - Snowflake: `"TABLE_NAME"` (case-sensitive, uppercase by default)

3. **Schema Inspection**:
   - SQLite: `SELECT name FROM sqlite_master WHERE type='table'`
   - Snowflake: `SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ?`
   - SQLite: `PRAGMA table_info(table_name)`
   - Snowflake: `SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ?`

4. **Data Types**:
   - SQLite TEXT → Snowflake VARCHAR
   - SQLite INTEGER → Snowflake NUMBER
   - SQLite REAL → Snowflake FLOAT
   - SQLite BLOB → Snowflake BINARY

5. **Connection Management**:
   - SQLite: Simple file-based, no connection pooling needed
   - Snowflake: Cloud-based, should use connection pooling for efficiency

### Security Considerations
- Store Snowflake credentials securely in `.env` file (not committed to git)
- Ensure `.env` is in `.gitignore`
- Use role-based access control in Snowflake (already using ACCOUNTADMIN role)
- Consider using Snowflake key pair authentication for production instead of password

### Performance Considerations
- Snowflake may have higher latency than SQLite for small queries (network overhead)
- Consider implementing connection pooling to reduce connection overhead
- Snowflake's query result caching may improve performance for repeated queries
- Use appropriate warehouse size for workload (currently configured to use "FOO" warehouse)

### Testing Strategy Notes
- Unit tests should mock Snowflake connections to avoid requiring live Snowflake instance
- Use `unittest.mock` or `pytest-mock` to mock `snowflake.connector.connect()`
- E2E test should use actual Snowflake connection with credentials from `.env`
- Consider creating a separate Snowflake schema for testing to avoid polluting production data

### Future Enhancements
- Implement connection pooling using `snowflake.connector.pooling`
- Add query performance monitoring and optimization
- Leverage Snowflake's semi-structured data support for native JSON handling
- Implement incremental data loading for large files
- Add support for Snowflake stages for bulk data loading
- Consider Snowflake's time travel features for data recovery
