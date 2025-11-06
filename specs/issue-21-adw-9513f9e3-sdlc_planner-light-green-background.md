# Chore: Background Color Update to Light Green

## Metadata
issue_number: `21`
adw_id: `9513f9e3`
issue_json: `{"number":21,"title":"Background color update","body":"/chore - adw_sdlc_zte_iso - Update the background color to the equivalent light green color "}`

## Chore Description
Update the application's background color from the current light sky blue (#E0F6FF) to an equivalent light green color. The goal is to provide a refreshed visual appearance while maintaining good readability, visual hierarchy, and compatibility with all existing UI components across the application.

## Relevant Files
Use these files to resolve the chore:

- **app/client/src/style.css** (line 9) - Contains the CSS root variables including the `--background` variable that controls the application's background color. This is the primary file to modify.
  - Currently set to `--background: #E0F6FF;` (light sky blue)
  - Needs to be updated to an equivalent light green color

- **app_docs/feature-6445fc8f-light-sky-blue-background.md** - Documentation reference showing the previous background color change pattern
- **app_docs/feature-f055c4f8-off-white-background.md** - Documentation reference showing background color update approach

### New Files
- **app_docs/chore-9513f9e3-light-green-background.md** - Documentation file to record this background color change following the established pattern

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Determine the Equivalent Light Green Color
- Research and select an appropriate light green hex color that matches the brightness and saturation level of the current light sky blue (#E0F6FF)
- Consider colors in the range of #E0FFE0 to #E8F8E8 for consistency with the light theme
- The chosen color should provide:
  - Similar luminosity to #E0F6FF
  - Good contrast with text and UI elements
  - A calming, professional appearance
  - Compatibility with existing white surfaces and UI components

### Step 2: Update the CSS Background Variable
- Open `app/client/src/style.css`
- Locate line 9 containing `--background: #E0F6FF;`
- Replace the value with the selected light green hex color
- Ensure no other CSS values need adjustment to maintain visual hierarchy

### Step 3: Verify Visual Compatibility
- Start the development server using `./scripts/start.sh`
- Visually inspect all major sections:
  - Query input section
  - Results display section
  - Tables list section
  - Modal dialogs
  - All buttons and interactive elements
- Confirm text readability and contrast
- Ensure white surface elements (cards, modals) stand out properly against the new background

### Step 4: Create Documentation
- Create `app_docs/chore-9513f9e3-light-green-background.md`
- Document the color change following the pattern from previous background color updates
- Include:
  - ADW ID and date
  - Overview of the change
  - Technical implementation details
  - The specific hex color chosen and rationale
  - Testing verification steps

### Step 5: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Verify the frontend builds successfully
- Confirm all server tests pass
- Validate the application starts without errors

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `cd app/client && bun run build` - Build the frontend to ensure no build errors with the CSS changes
- `./scripts/start.sh` - Start the application to verify it runs without errors (manual verification step)

## Notes
- The previous background color was light sky blue (#E0F6FF), implemented in issue #15 (ADW ID: 6445fc8f)
- Before that, the background was off-white (#fafafa), from issue #12 (ADW ID: f055c4f8)
- The application uses a CSS variable system, so changing `--background` will update the color across the entire application
- Consider light green colors like:
  - #E0FFE8 (very light mint green)
  - #E8F8E8 (pale green)
  - #E0F8E0 (light pastel green)
- The selected color should have similar RGB values to #E0F6FF (224, 246, 255) for equivalent lightness
- All existing UI components are designed to work with light backgrounds, so minimal adjustment should be needed
- The body element uses `background: var(--background);` on line 30 of style.css
