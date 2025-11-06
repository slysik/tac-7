# E2E Test: Random Query Generation

Test the LLM-based random query generation functionality in the Natural Language SQL Interface application.

## User Story

As a user
I want to generate random natural language queries based on my data schema
So that I can explore query capabilities and get inspiration for questions to ask

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
7. Use sample data or upload a test JSON/CSV file (e.g., users.json with at least 1 row)
8. **Verify** the table appears in the "Available Tables" section
9. Take a screenshot of the table

10. **Verify** the "Generate Random Query" button appears (should be visible near the query input area)
11. Take a screenshot showing the Generate Random Query button clearly visible
12. **Verify** the query input field is empty or has existing content

13. Click the "Generate Random Query" button
14. **Verify** loading state appears (button may show spinner or be disabled briefly)
15. Take a screenshot of the loading state if visible

16. Wait for completion (up to 10 seconds for LLM response)
17. **Verify** a random natural language query appears in the query input field
18. Take a screenshot of the query input with the generated query

19. **Verify** the generated query is:
    - Contextually relevant to the uploaded table structure and columns
    - Natural and conversational (not SQL syntax)
    - Maximum two sentences
    - Does NOT contain SQL comments (-- or /* */)
    - Does NOT contain SQL syntax like SELECT, FROM, WHERE, etc.

20. **Verify** no error messages appear
21. Take a screenshot showing no errors

22. Click the "Query" button to execute the generated query
23. **Verify** the query executes successfully without errors
24. **Verify** results appear (SQL translation and data table)
25. Take a screenshot of the successful query execution

26. Click "Generate Random Query" button again
27. **Verify** a different query is generated (may be similar but should show variety)
28. Take a screenshot of the second generated query

## Success Criteria

- "Generate Random Query" button is visible and clickable
- Clicking the button generates a natural language query
- Generated query appears in the query input field
- Query is contextually relevant to the uploaded data schema
- Query is natural language (not SQL syntax)
- Query does not contain SQL comments or special characters
- No errors occur during generation (no 400 error about max_tokens parameter)
- Generated query can be successfully executed when clicking "Query" button
- Multiple clicks generate varied queries
- At least 7 screenshots are taken demonstrating the feature

## Notes

- This test requires a valid OpenAI or Anthropic API key to be configured in the backend
- The application must have at least one table with data uploaded
- Generated queries should demonstrate variety in complexity (simple, complex with JOINs, aggregations)
- This test specifically validates the fix for the `max_tokens` → `max_completion_tokens` parameter change
- If a 400 error occurs mentioning "Unsupported parameter: 'max_tokens'", the test fails
