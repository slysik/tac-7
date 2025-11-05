# E2E Test: CSV Export Text Consistency

Test that CSV export button text is consistent across Available Tables and Query Results sections.

## User Story

As a user
I want to see consistent CSV export button labels throughout the application
So that I have a clear understanding of the export functionality

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** the Available Tables section is visible

5. Upload sample data (users.json) by:
   - Click "Upload Data" button
   - Click "users.json" sample data button
   - Wait for table to be created
6. Take a screenshot showing the Available Tables section
7. **Verify** the table export button in Available Tables section displays "📊 CSV Export"
8. Take a screenshot focused on the table export button showing the text "📊 CSV Export"

9. Enter the query: "Show me all users from the users table"
10. Click the Query button
11. Wait for query results to appear
12. Take a screenshot showing the Query Results section
13. **Verify** the export button in Query Results section displays "📊 CSV Export"
14. Take a screenshot focused on the query results export button showing the text "📊 CSV Export"

15. **Verify** both export buttons display identical text: "📊 CSV Export"

## Success Criteria
- Available Tables section CSV export button displays "📊 CSV Export"
- Query Results section CSV export button displays "📊 CSV Export"
- Both buttons have identical, consistent text
- 5 screenshots are taken showing the consistency
