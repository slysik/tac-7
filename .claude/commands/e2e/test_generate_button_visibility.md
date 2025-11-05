# E2E Test: Generate Data Button Visibility

Test that the Generate Data button appears correctly in the Available Tables section after uploading data.

## User Story

As a user
I want to see the Generate Data button for each table I upload
So that I can generate synthetic data when needed

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** the page loads successfully (no console errors for /api/schema endpoint)
5. **Verify** core UI elements are present:
   - Query input textbox
   - Upload Data button
   - Available Tables section

6. Click the "Upload Data" button
7. Take a screenshot of the upload modal
8. **Verify** the upload modal appears with sample data options

9. Click "👥 Users Data" to upload sample users data
10. **Verify** the "users" table appears in the Available Tables section
11. **Verify** the table shows row count (e.g., "20 rows, 6 columns")
12. Take a screenshot showing the users table with buttons

13. **Verify** the "⚡ Generate" button is visible in the table header
14. **Verify** the Generate button is positioned to the left of the CSV Export button
15. **Verify** the Generate button has a lightning bolt emoji (⚡)
16. Take a close-up screenshot of the button area

17. Hover over the Generate button
18. **Verify** tooltip appears with text "Generate synthetic data using AI"
19. Take a screenshot showing the tooltip

## Success Criteria
- Application loads without connection errors
- Upload modal displays sample data options
- Users table appears after upload with correct row/column count
- Generate Data button is visible with lightning bolt icon (⚡)
- Button is positioned correctly (left of CSV Export button)
- Button has proper tooltip text
- All screenshots are captured successfully
