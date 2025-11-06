# Feature: Enhanced Drag-and-Drop Surface Area for Data Upload

## Metadata
issue_number: `1`
adw_id: `7c9020a6`
issue_json: `{"number":1,"title":"increase drop zone surface area","body":"/feature\n\nadw_sdlc_iso\n\nlets increase the drop zone surface area. instead of having to click \"upload data\". The user can drag and drop right on to the upper div or lower fiv and the ui will update to a 'drop to create table' text. This runs the same usual functionality but enhances the ui to be more user friendly.  "}`

## Feature Description
This feature enhances the user experience by expanding the drag-and-drop functionality beyond the current modal-only upload zone. Users will be able to drag files directly onto the query section (upper div) and tables section (lower div) on the main page. When dragging over these areas, visual feedback will change the UI text to "Drop to create table", making the upload process more intuitive and eliminating the need to explicitly click the "Upload" button first.

## User Story
As a user
I want to drag and drop files directly onto the main page areas
So that I can upload data more quickly without opening the upload modal first

## Problem Statement
Currently, users must click the "Upload" button to open a modal before they can drag and drop files. This adds an unnecessary step to the workflow. The drag-and-drop zone is limited to a small area within the modal, reducing the user-friendly nature of the interface. Users expect modern web applications to accept file drops on larger surface areas.

## Solution Statement
We will add drag-and-drop event listeners to the query section and tables section divs on the main page. When a user drags a file over these areas, the UI will provide visual feedback by updating text to "Drop to create table". Upon drop, the file will be uploaded using the existing file upload handler, bypassing the need to open the modal. The existing modal functionality will remain unchanged for users who prefer the traditional upload button approach.

## Relevant Files
Use these files to implement the feature:

- `app/client/index.html` (lines 14-47) - Contains the query section and tables section divs that need to become drop zones
  - Query section: `<section id="query-section" class="query-section">` (line 15)
  - Tables section: `<section id="tables-section" class="tables-section">` (line 42)

- `app/client/src/main.ts` (lines 122-174) - Contains the existing file upload functionality
  - `initializeFileUpload()` function (line 123) - Handles current modal-based drag and drop
  - `handleFileUpload()` function (line 161) - Processes file uploads and should be reused

- `app/client/src/style.css` - Contains styles for sections and drag states
  - Query section styles (lines 55-93)
  - Tables section styles (lines 226-245)
  - Drop zone dragover styles (lines 255-258) - Can be adapted for main sections
  - Need to add new styles for drag-over states on query and tables sections

### New Files
- `.claude/commands/e2e/test_enhanced_drag_drop.md` - E2E test file to validate the enhanced drag-and-drop functionality

## Implementation Plan

### Phase 1: Foundation
1. Review existing drag-and-drop implementation in the modal to understand the event handling patterns
2. Identify reusable components and handlers from the current implementation
3. Plan the visual feedback mechanism for the enhanced drop zones

### Phase 2: Core Implementation
1. Add drag-and-drop event listeners to query section and tables section
2. Implement visual feedback (text change to "Drop to create table") during drag-over state
3. Connect drop events to the existing `handleFileUpload()` function
4. Add CSS styles for the new drag-over states on main sections

### Phase 3: Integration
1. Test that the new drag-and-drop functionality coexists with the existing modal-based upload
2. Ensure consistent behavior across both upload methods
3. Verify that file validation and error handling work the same way
4. Create comprehensive E2E tests to validate the feature

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Create E2E Test File
Create the E2E test specification that defines the expected behavior for the enhanced drag-and-drop feature. This test will:
- Verify drag-over visual feedback on query section
- Verify drag-over visual feedback on tables section
- Verify file upload works from query section
- Verify file upload works from tables section
- Verify table creation and schema loading after drop
- Take screenshots at key states

Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` to understand the E2E test format, then create `.claude/commands/e2e/test_enhanced_drag_drop.md`.

### Task 2: Add CSS Styles for Enhanced Drop Zones
Update `app/client/src/style.css` to add styles for the drag-over states on the query and tables sections:
- Add `.query-section.dragover` class with visual feedback styling
- Add `.tables-section.dragover` class with visual feedback styling
- Add `.drop-message` class for the "Drop to create table" text overlay
- Consider using a semi-transparent overlay with centered text
- Use consistent styling with the existing modal drop zone

### Task 3: Implement Enhanced Drag-Drop for Query Section
Update `app/client/src/main.ts` to add drag-and-drop functionality to the query section:
- Add a new function `initializeEnhancedDropZones()` to be called from `DOMContentLoaded`
- Get reference to `query-section` element
- Add `dragover` event listener that prevents default and adds visual feedback
- Add `dragleave` event listener to remove visual feedback
- Add `drop` event listener that:
  - Prevents default behavior
  - Removes visual feedback
  - Extracts files from `dataTransfer`
  - Calls existing `handleFileUpload()` function
- Handle edge cases like dragging non-file items

### Task 4: Implement Enhanced Drag-Drop for Tables Section
Update `app/client/src/main.ts` to add drag-and-drop functionality to the tables section:
- Get reference to `tables-section` element in the `initializeEnhancedDropZones()` function
- Add the same drag event listeners as query section (dragover, dragleave, drop)
- Reuse the same visual feedback mechanism
- Ensure consistent behavior between both drop zones

### Task 5: Add Visual Feedback Overlay
Update `app/client/src/main.ts` to implement the "Drop to create table" text overlay:
- Create helper function `showDropOverlay(element: HTMLElement)` that:
  - Creates a div with class `drop-message`
  - Sets text content to "Drop to create table"
  - Appends to the target element
  - Returns the overlay element for later removal
- Create helper function `hideDropOverlay(element: HTMLElement)` that:
  - Finds and removes the `drop-message` element
- Use these helpers in the dragover/dragleave/drop event handlers

### Task 6: Handle Edge Cases and Validation
Update the drag-and-drop handlers to include:
- File type validation (only accept .csv, .json, .jsonl)
- Visual indication when dragging invalid file types
- Prevent drops when invalid files are detected
- Handle multiple file drops (only process the first file)
- Ensure drag events don't interfere with text selection in query input

### Task 7: Test Integration with Existing Upload Modal
Verify that the new functionality doesn't break existing features:
- Test that modal-based upload still works
- Test that both upload methods produce identical results
- Test that error handling is consistent across both methods
- Verify file validation works the same way

### Task 8: Run Validation Commands
Execute all validation commands to ensure the feature works correctly with zero regressions.

## Testing Strategy

### Unit Tests
While this is primarily a UI feature that will be validated through E2E tests, ensure that:
- Existing server-side file upload endpoint tests still pass
- File validation logic on the server remains unchanged
- Database table creation logic is not affected

### Edge Cases
Test the following edge cases:
1. Dragging non-file items (text, links) over the drop zones
2. Dragging multiple files and dropping (should handle only the first)
3. Dragging unsupported file types (.txt, .pdf, etc.)
4. Dragging files while a query is in progress
5. Dragging files when the upload modal is already open
6. Rapid successive drag-and-drop operations
7. Dragging over nested elements within the sections
8. Browser compatibility (drag events may vary slightly)

## Acceptance Criteria
- Users can drag files over the query section and see "Drop to create table" feedback
- Users can drag files over the tables section and see "Drop to create table" feedback
- Dropping a valid file (.csv, .json, .jsonl) on either section uploads the file successfully
- Invalid file types show appropriate validation errors
- Visual feedback appears and disappears correctly during drag operations
- The existing modal-based upload functionality remains fully functional
- File upload behavior is identical whether uploaded via modal or enhanced drop zones
- E2E test passes with all verification steps successful
- No regressions in existing upload functionality
- UI remains responsive during drag operations
- Visual feedback is clear and consistent with existing design patterns

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the E2E test file `.claude/commands/e2e/test_enhanced_drag_drop.md` to validate the enhanced drag-and-drop functionality works as expected
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend TypeScript checks to validate no type errors
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### Design Considerations
- The visual feedback should be obvious but not jarring
- Consider using a semi-transparent overlay to avoid covering important UI elements completely
- The "Drop to create table" message should be large enough to read clearly
- Maintain accessibility by ensuring drag-and-drop doesn't break keyboard navigation

### Future Enhancements
Consider these potential improvements for future iterations:
- Show file type icons during drag to indicate supported formats
- Add animation to the overlay appearance/disappearance
- Display a preview of the file name during drag
- Support drag-and-drop reordering of tables in the tables section
- Add multi-file upload support with batch processing

### Technical Notes
- The existing `handleFileUpload()` function is well-tested and should be reused without modification
- Drag events can bubble, so use `stopPropagation()` where needed to prevent multiple handlers firing
- The `dataTransfer.files` API provides access to dropped files
- Use `dataTransfer.types` to check if dragged content contains files before showing feedback
- Test with both mouse drag and touch drag on supported devices
