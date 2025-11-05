# E2E Test: Synthetic Data Generation

Test the LLM-based synthetic data generation functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate realistic synthetic data for my tables using AI
So that I can quickly expand my datasets for testing and development

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Available Tables section

5. Click "Upload Data" button to open the upload modal
6. Take a screenshot of the upload modal
7. Use sample data or upload a test JSON file (e.g., users.json with at least 1 row)
8. **Verify** the table appears in the "Available Tables" section
9. Take a screenshot of the table with initial row count

10. **Verify** the "⚡ Generate" button appears next to the table (left of CSV export button)
11. Take a screenshot showing the Generate Data button clearly visible
12. Note the initial row count displayed (e.g., "5 rows")

13. Click the "⚡ Generate" button
14. **Verify** loading state appears (button shows spinner and is disabled)
15. Take a screenshot of the loading state

16. Wait for completion (up to 30 seconds for LLM response)
17. **Verify** success notification appears showing "Generated 10 rows for table '[table_name]'"
18. Take a screenshot of the success notification

19. **Verify** the table row count has increased by 10 rows (e.g., from "5 rows" to "15 rows")
20. Take a screenshot showing the updated row count

21. Enter a query to view the new data: "Show me all records from [table_name]"
22. Click the Query button
23. **Verify** the results contain the newly generated synthetic data
24. Take a screenshot of query results showing the synthetic data

25. **Verify** generated data matches expected patterns:
    - Emails have realistic domains (gmail.com, yahoo.com, outlook.com)
    - Names are diverse and realistic (not "User 1", "User 2", etc.)
    - Data types match the schema (integers are integers, text is text)
    - Nullable columns may contain null values if sample data had them

26. Take a screenshot of a few sample rows demonstrating realistic data patterns

## Success Criteria

- "⚡ Generate" button appears for each table
- Button is positioned to the left of the CSV export button
- Loading state appears when button is clicked (button disabled, spinner visible)
- Generation completes within 30 seconds
- Success notification shows "Generated 10 rows" message
- Table row count increases by exactly 10
- Generated data is visible when querying the table
- Data matches schema and shows realistic patterns (not repetitive)
- Data has variety (different names, emails, values)
- At least 6 screenshots are taken demonstrating the feature

## Notes

- This test requires a valid OpenAI or Anthropic API key to be configured in the backend
- The table must have at least 1 existing row for generation to work
- If the table is empty, the button should still be visible but clicking it should show an error message
- Generated data should be contextually relevant to the existing data patterns
