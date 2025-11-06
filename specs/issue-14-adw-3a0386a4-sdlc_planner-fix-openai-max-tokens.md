# Bug: Fix OpenAI max_tokens Parameter Error

## Metadata
issue_number: `14`
adw_id: `3a0386a4`
issue_json: `{"number":14,"title":"Error generating random query with OpenAI:","body":"bug - adw_patch_iso - \nError generating random query with OpenAI:\n\nError generating random query with OpenAI: Error code: 400 - {'error': {'message': \"Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.\", 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': 'unsupported_parameter'}}\n\n\nFix this issue.\n"}`

## Bug Description
The application fails when generating random queries with OpenAI's o4-mini-2025-04-16 model. The error indicates that the `max_tokens` parameter is not supported by this model and must be replaced with `max_completion_tokens`. This error occurs in the `/api/generate-random-query` endpoint when using the OpenAI provider.

Expected behavior: Random query generation should work without errors.
Actual behavior: API returns 400 error with message about unsupported `max_tokens` parameter.

## Problem Statement
OpenAI's o4-mini model series requires `max_completion_tokens` instead of `max_tokens` for limiting response length. The current implementation in `app/server/core/llm_processor.py` uses the deprecated `max_tokens` parameter in all OpenAI API calls, causing 400 errors when using the o4-mini-2025-04-16 model.

## Solution Statement
Replace all instances of `max_tokens` with `max_completion_tokens` in OpenAI API calls within the `llm_processor.py` module. This change will ensure compatibility with OpenAI's o4-mini model while maintaining the same token limiting behavior.

## Steps to Reproduce
1. Start the application with `./scripts/start.sh`
2. Ensure `OPENAI_API_KEY` is set in `app/server/.env`
3. Upload sample data (e.g., CSV file with users table)
4. Click the "Generate Random Query" button (or call `/api/generate-random-query` endpoint)
5. Observe the 400 error: "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead."

## Root Cause Analysis
The OpenAI o4-mini model series introduced a breaking change where `max_tokens` is no longer supported and must be replaced with `max_completion_tokens`. The application was upgraded to use the o4-mini-2025-04-16 model (as documented in `app_docs/feature-4c768184-model-upgrades.md`), but the parameter names were not updated to match the new API requirements.

The issue affects three functions in `app/server/core/llm_processor.py`:
1. `generate_sql_with_openai` (line 51) - uses `max_tokens=500`
2. `generate_random_query_with_openai` (line 191) - uses `max_tokens=100`
3. `generate_synthetic_data_with_openai` (line 354) - uses `max_tokens=2000`

## Relevant Files
Use these files to fix the bug:

- `app/server/core/llm_processor.py` - Contains all OpenAI API calls that use the deprecated `max_tokens` parameter. Need to replace `max_tokens` with `max_completion_tokens` in three functions:
  - `generate_sql_with_openai` (line 44-52)
  - `generate_random_query_with_openai` (line 184-192)
  - `generate_synthetic_data_with_openai` (line 347-355)

- `app/server/tests/core/test_llm_processor.py` - Contains unit tests that verify the OpenAI API calls. Need to update test assertions to check for `max_completion_tokens` instead of `max_tokens`:
  - `test_generate_sql_with_openai_success` (line 46)

- `README.md` - Project documentation for reference on how to run the application and tests

### New Files
- `.claude/commands/e2e/test_random_query_generation.md` - E2E test to validate random query generation works correctly

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update OpenAI API calls in llm_processor.py
- Replace `max_tokens` with `max_completion_tokens` in `generate_sql_with_openai` function (line 51)
- Replace `max_tokens` with `max_completion_tokens` in `generate_random_query_with_openai` function (line 191)
- Replace `max_tokens` with `max_completion_tokens` in `generate_synthetic_data_with_openai` function (line 354)

### 2. Update test assertions
- Update `test_generate_sql_with_openai_success` in `app/server/tests/core/test_llm_processor.py` to assert `max_completion_tokens` instead of `max_tokens` (line 46)

### 3. Create E2E test for random query generation
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_synthetic_data_generation.md` to understand E2E test format
- Create `.claude/commands/e2e/test_random_query_generation.md` that validates:
  - User uploads sample data
  - User clicks "Generate Random Query" button
  - A random query is generated without errors
  - The generated query is displayed in the query input field
  - Include screenshots to prove the functionality works

### 4. Run validation commands
- Execute all commands listed in the `Validation Commands` section to validate the bug is fixed with zero regressions

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

### Manual verification of the fix
1. Start the application: `./scripts/start.sh`
2. Upload sample data via the UI
3. Click "Generate Random Query" button
4. Verify no errors occur and a query is generated

### Automated tests
- `cd app/server && uv run pytest tests/core/test_llm_processor.py::TestLLMProcessor::test_generate_sql_with_openai_success -v` - Verify OpenAI API parameter changes work correctly
- `cd app/server && uv run pytest` - Run all server tests to validate the bug is fixed with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate no regressions
- `cd app/client && bun run build` - Run frontend build to validate no regressions

### E2E test
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_random_query_generation.md` to validate this functionality works

## Notes
- This is a minimal, surgical fix targeting only the parameter name change
- The fix applies to all three OpenAI functions that generate text: SQL queries, random queries, and synthetic data
- GPT-4.1 model also uses `max_completion_tokens`, so this change is consistent across OpenAI's latest models
- Anthropic's Claude models continue to use `max_tokens`, so no changes are needed for Anthropic API calls
- The token limits themselves (500, 100, 2000) remain unchanged
