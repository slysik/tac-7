# E2E Test: OpenAI max_completion_tokens Parameter Validation

Test that OpenAI API calls work correctly with the max_completion_tokens parameter in the Natural Language SQL Interface application.

## User Story

As a user
I want to use OpenAI for SQL generation, random query generation, and synthetic data generation
So that I can leverage OpenAI's capabilities with the correct API parameters

## Prerequisites

- OPENAI_API_KEY environment variable must be set
- Application should prioritize OpenAI when both OpenAI and Anthropic keys are available

## Test Steps

### Test SQL Query Generation with OpenAI

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Available Tables section

5. Click the Upload Data button
6. Click on the "Users Data" sample button
7. **Verify** the users table appears in Available Tables
8. Take a screenshot of the tables section

9. Enter the query: "Show me all users who signed up in the last month"
10. Take a screenshot of the query input
11. Click the Query button
12. **Verify** the query executes successfully without OpenAI API errors
13. **Verify** the SQL translation is displayed
14. **Verify** the results table contains data (or "No results" message is shown)
15. Take a screenshot of the SQL translation and results
16. Click "Hide" button to close results

### Test Random Query Generation with OpenAI

17. Click the Generate Random Query button
18. **Verify** a natural language query is generated without OpenAI API errors
19. **Verify** the generated query is relevant to the users table
20. Take a screenshot of the generated query

21. Click the Query button to execute the generated query
22. **Verify** the query executes successfully
23. **Verify** the SQL translation is displayed
24. **Verify** the results table contains data
25. Take a screenshot of the executed query results
26. Click "Hide" button to close results

### Test Synthetic Data Generation with OpenAI

27. Click on the users table in the Available Tables section to expand it
28. **Verify** the "Generate Data" button is visible
29. Take a screenshot of the expanded table with the Generate Data button

30. Click the "Generate Data" button
31. **Verify** a success message appears (or synthetic data is generated without OpenAI API errors)
32. **Verify** the table row count increases by 10 (or generation completes successfully)
33. Take a screenshot of the generation result

34. Enter the query: "Show me the 10 most recent users"
35. Click the Query button
36. **Verify** the query executes successfully
37. **Verify** synthetic data is visible in the results (check for realistic variety)
38. Take a screenshot of the synthetic data results

## Success Criteria

- SQL query generation works without OpenAI API parameter errors
- Random query generation works without OpenAI API parameter errors
- Synthetic data generation works without OpenAI API parameter errors
- No 400 errors about "Unsupported parameter: 'max_tokens'"
- All OpenAI functionality produces expected results
- 8 screenshots are taken

## Error Scenarios to Avoid

- Should NOT see: "Unsupported parameter: 'max_tokens' is not supported with this model"
- Should NOT see: "Use 'max_completion_tokens' instead"
- Should NOT see: 400 error codes from OpenAI API
