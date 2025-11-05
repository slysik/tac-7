# Bug: CSV Export Button Text Mismatch

## Metadata
issue_number: `5`
adw_id: `88e60dd3`
issue_json: `{"number":5,"title":"\"CSV\" texts don't match","body":"bug - adw_patch_iso - Under available tables section the csv export button has the correct text \"📊 CSV Export\".\n\nUpdate the query result section csv export button text should match this.  "}`

## Bug Description
There is an inconsistency in the CSV export button text between the available tables section and the query results section. According to the bug report, the available tables section displays the correct text "📊 CSV Export", but the query results section has different text that needs to be updated to match.

Upon code inspection, the actual situation is:
- Available tables section (line 340 in main.ts): Shows "📊 CSV" (missing "Export" text)
- Query results section (line 242 in main.ts): Shows "📊 CSV Export" (has full text)

The bug report indicates that "📊 CSV Export" is the correct format, meaning we need to update the available tables section to include " Export" text to match the query results section.

## Problem Statement
The CSV export buttons across the application have inconsistent text labels. The available tables section only displays "📊 CSV" while it should display "📊 CSV Export" to match the query results section and provide clear user guidance.

## Solution Statement
Update the `getDownloadIcon()` function in `app/client/src/main.ts` to return "📊 CSV Export" instead of "📊 CSV", ensuring consistent labeling across both the available tables section and query results section. This change will make the export functionality more explicit and user-friendly.

## Steps to Reproduce
1. Start the application using `./scripts/start.sh`
2. Navigate to http://localhost:5173
3. Upload sample data (e.g., users.json) to create a table
4. Observe the CSV export button in the "Available Tables" section - it shows "📊 CSV"
5. Execute a query that returns results
6. Observe the CSV export button in the "Query Results" section - it shows "📊 CSV Export"
7. Notice the inconsistency between the two button labels

## Root Cause Analysis
The `getDownloadIcon()` helper function at line 16-18 in `app/client/src/main.ts` returns only "📊 CSV" without the "Export" suffix. This function is used in:
1. Line 340: Table export button in the available tables section
2. Line 242: Query results export button (but with " Export" appended via template literal)

The inconsistency exists because the query results section manually appends " Export" to the icon text (line 242: `${getDownloadIcon()} Export`), while the table export button uses only the return value of `getDownloadIcon()` (line 340: `getDownloadIcon()`).

The correct approach is to have `getDownloadIcon()` return the complete text "📊 CSV Export" so both sections display consistent text.

## Relevant Files
Use these files to fix the bug:

- **app/client/src/main.ts** (lines 16-18, 242, 340)
  - Contains the `getDownloadIcon()` function that needs to be updated
  - Line 16-18: Helper function that returns the CSV export icon text
  - Line 242: Query results export button that currently appends " Export"
  - Line 340: Table export button that uses getDownloadIcon() directly

- **README.md**
  - Project overview and structure for context

- **app_docs/feature-490eb6b5-one-click-table-exports.md**
  - Documentation for the CSV export feature to understand intended behavior

### New Files
- **.claude/commands/e2e/test_csv_export_text_consistency.md**
  - E2E test to validate CSV export button text is consistent across both sections

## Step by Step Tasks

### 1. Update getDownloadIcon() function
- Modify the `getDownloadIcon()` function in `app/client/src/main.ts` (line 16-18) to return "📊 CSV Export" instead of "📊 CSV"
- This ensures the complete text is returned from a single source of truth

### 2. Update query results export button
- Update line 242 in `app/client/src/main.ts` to use only `getDownloadIcon()` instead of `${getDownloadIcon()} Export`
- Remove the redundant " Export" text since it's now included in the function return value
- This maintains the same display text while eliminating duplication

### 3. Create E2E test file
- Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand the E2E test structure
- Create a new E2E test file `.claude/commands/e2e/test_csv_export_text_consistency.md`
- The test should validate that:
  - Upload sample data and verify the table export button shows "📊 CSV Export"
  - Execute a query with results and verify the query results export button shows "📊 CSV Export"
  - Both buttons display identical text
  - Take screenshots proving both buttons have consistent text

### 4. Run validation commands
- Execute all validation commands listed below to ensure the bug is fixed with zero regressions
- Verify TypeScript compilation succeeds
- Verify frontend build succeeds
- Run E2E test to validate button text consistency

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_csv_export_text_consistency.md` test file to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the bug is fixed with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the bug is fixed with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the bug is fixed with zero regressions

## Notes
- This is a frontend-only change affecting UI text consistency
- No server-side changes are required
- No new dependencies needed
- The change improves user experience by providing clear, consistent labeling across all CSV export buttons
- The fix follows the single source of truth principle by centralizing the button text in one function
- Both table exports and query result exports will display the same clear "📊 CSV Export" text
