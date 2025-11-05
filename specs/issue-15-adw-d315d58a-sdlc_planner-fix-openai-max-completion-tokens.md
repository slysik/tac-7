# Bug: Fix OpenAI max_completion_tokens Parameter Error

## Metadata
issue_number: `15`
adw_id: `d315d58a`
issue_json: `{"number":15,"title":"Error generating random query with OpenAI","body":"bug - adw_patch_iso -\nError generating random query with OpenAI:\n\nError generating random query with OpenAI: Error code: 400 - {'error': {'message': \"Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead.\", 'type': 'invalid_request_error', 'param': 'max_tokens', 'code': 'unsupported_parameter'}}\n\nbranch bug-issue-14-adw-ef072df6-fix-openai-max-tokens-param \n\n fix the OpenAI API parameter error (max_tokens vs max_completion_tokens)."}`

## Bug Description
The application fails when generating random natural language queries using the OpenAI API. The error occurs because the newer OpenAI model `o4-mini-2025-04-16` no longer supports the `max_tokens` parameter and requires using `max_completion_tokens` instead. This causes a 400 error with the message: "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead."

## Problem Statement
The `llm_processor.py` module uses the deprecated `max_tokens` parameter in three OpenAI API calls:
1. SQL generation (line 51)
2. Random query generation (line 191)
3. Synthetic data generation (line 354)

This causes the API to reject requests when using the newer `o4-mini-2025-04-16` model, breaking random query generation and potentially other OpenAI-dependent features.

## Solution Statement
Replace all occurrences of the `max_tokens` parameter with `max_completion_tokens` in the OpenAI API calls within `llm_processor.py`. Update corresponding test assertions to verify the correct parameter is being used. Validate the fix using existing E2E tests for random query generation.

## Steps to Reproduce
1. Start the application with a valid OpenAI API key set
2. Upload sample data (e.g., Users Data)
3. Click the "Generate Random Query" button
4. Observe the 400 error: "Unsupported parameter: 'max_tokens' is not supported with this model. Use 'max_completion_tokens' instead."

## Root Cause Analysis
The OpenAI API has evolved and newer models (including `o4-mini-2025-04-16` used in the codebase) have changed their parameter naming conventions. The `max_tokens` parameter was renamed to `max_completion_tokens` to better reflect its purpose (controlling completion length rather than total tokens). The codebase was upgraded to use `o4-mini-2025-04-16` in a previous feature (see app_docs/feature-4c768184-model-upgrades.md) but the parameter names were not updated to match the new model's requirements.

## Relevant Files
Use these files to fix the bug:

- `app/server/core/llm_processor.py` (lines 51, 191, 354) - Contains three OpenAI API calls using the deprecated `max_tokens` parameter that need to be updated to `max_completion_tokens`
- `app/server/tests/core/test_llm_processor.py` (line 46) - Contains test assertion that verifies `max_tokens` parameter, needs to be updated to verify `max_completion_tokens` instead
- `.claude/commands/e2e/test_random_query_generator.md` - E2E test that validates the random query generation functionality affected by this bug
- `.claude/commands/test_e2e.md` - E2E test execution framework for validating the fix

### New Files

- `.claude/commands/e2e/test_openai_max_completion_tokens.md` - New E2E test to specifically validate that OpenAI API calls work correctly with the max_completion_tokens parameter

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update OpenAI API Calls in llm_processor.py
- Replace `max_tokens=500` with `max_completion_tokens=500` in `generate_sql_with_openai()` function (line 51)
- Replace `max_tokens=100` with `max_completion_tokens=100` in `generate_random_query_with_openai()` function (line 191)
- Replace `max_tokens=2000` with `max_completion_tokens=2000` in `generate_synthetic_data_with_openai()` function (line 354)

### 2. Update Test Assertions
- Update test assertion in `test_llm_processor.py` line 46 from `assert call_args[1]['max_tokens'] == 500` to `assert call_args[1]['max_completion_tokens'] == 500`

### 3. Create E2E Test for OpenAI Parameter Validation
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_random_query_generator.md` to understand the E2E test format
- Create a new E2E test file `.claude/commands/e2e/test_openai_max_completion_tokens.md` that:
  - Validates that SQL query generation works with OpenAI
  - Validates that random query generation works with OpenAI
  - Validates that synthetic data generation works with OpenAI (if a generate button is available)
  - Takes screenshots to prove the functionality works
  - Tests specifically with OpenAI API (not Anthropic) to ensure the parameter fix is working

### 4. Run Validation Commands
Execute all validation commands listed below to ensure the bug is fixed with zero regressions.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Run LLM processor tests to validate the parameter changes
- `cd app/server && uv run pytest` - Run all server tests to validate no regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript type checking to validate no frontend regressions
- `cd app/client && bun run build` - Run frontend build to validate no build errors
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_random_query_generator.md` to validate that random query generation works correctly with OpenAI
- Read `.claude/commands/test_e2e.md`, then read and execute your new `.claude/commands/e2e/test_openai_max_completion_tokens.md` test file to validate that all OpenAI functionality works with the new parameter

## Notes
- This bug was introduced when the model was upgraded to `o4-mini-2025-04-16` without updating the parameter names to match the new API requirements
- Only OpenAI API calls need to be updated; Anthropic API calls use `max_tokens` correctly
- The fix is a simple parameter rename with no logic changes required
- All three affected functions maintain the same token limits (500, 100, and 2000 respectively)
- The E2E test for random query generation already exists and will validate the most visible symptom of this bug
- This is a minimal, surgical fix that only changes the parameter name in three locations plus one test assertion
