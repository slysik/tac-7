# E2E Test: Enhanced Drag-and-Drop Surface Area

Test the enhanced drag-and-drop functionality that allows users to drop files directly onto the query section and tables section.

## User Story

As a user
I want to drag and drop files directly onto the main page areas
So that I can upload data more quickly without opening the upload modal first

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input section (#query-section)
   - Tables section (#tables-section)
   - Upload Data button

5. Create a test CSV file with sample data:
   - File name: "test_drag_drop.csv"
   - Content: "id,name,age\n1,Alice,30\n2,Bob,25\n3,Charlie,35"
   - Save to a temporary location

6. Get absolute path to the test CSV file for drag-and-drop

7. Simulate drag over query section:
   - Take a screenshot before drag
   - Trigger dragover event on #query-section
   - **Verify** visual feedback appears (dragover class or overlay with "Drop to create table" text)
   - Take a screenshot showing drag feedback
   - Trigger dragleave event
   - **Verify** visual feedback disappears

8. Simulate drag over tables section:
   - Trigger dragover event on #tables-section
   - **Verify** visual feedback appears (dragover class or overlay with "Drop to create table" text)
   - Take a screenshot showing drag feedback
   - Trigger dragleave event
   - **Verify** visual feedback disappears

9. Perform actual file drop on query section:
   - Upload the test CSV file to #query-section using file input simulation
   - Wait for upload to complete (look for table in Available Tables section)
   - **Verify** the table "test_drag_drop" appears in Available Tables
   - Take a screenshot showing the uploaded table
   - **Verify** schema is displayed (columns: id, name, age)

10. Clean up by removing the uploaded table if possible (optional)

11. Perform actual file drop on tables section:
    - Create a second test CSV file: "test_drag_drop_2.csv" with content "id,product,price\n1,Widget,9.99\n2,Gadget,19.99"
    - Upload the second test CSV file to #tables-section
    - Wait for upload to complete
    - **Verify** the table "test_drag_drop_2" appears in Available Tables
    - Take a screenshot showing both tables
    - **Verify** schema is displayed for the new table (columns: id, product, price)

12. Test that existing upload modal still works:
    - Click "Upload Data" button
    - **Verify** modal opens
    - Take a screenshot of the modal
    - Close the modal

## Success Criteria
- Query section accepts drag events and shows visual feedback
- Tables section accepts drag events and shows visual feedback
- Visual feedback ("Drop to create table") appears during dragover
- Visual feedback disappears on dragleave
- Files dropped on query section are uploaded successfully
- Files dropped on tables section are uploaded successfully
- Tables appear in Available Tables section after drop
- Schema is loaded and displayed for uploaded tables
- Existing modal-based upload remains functional
- At least 6 screenshots are taken showing key states
