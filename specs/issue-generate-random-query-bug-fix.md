# Bug: Generate Random Query Not Working

## Metadata
issue_number: `unknown`
adw_id: `unknown`
issue_json: `{"title": "Generate Random Query not working", "body": "The 'Generate Random Query' button is not working properly"}`

## Bug Description
The "Generate Random Query" button in the UI is not functioning correctly. When clicked, the feature fails to generate a random query. The root cause is an invalid Anthropic model name being used in the LLM processor that doesn't exist in the Anthropic API, combined with an unsupported `temperature` parameter in the Anthropic messages API call.

## Problem Statement
The `generate_random_query_with_anthropic()` function in `app/server/core/llm_processor.py` uses an invalid model name `"claude-sonnet-4-0"` which doesn't exist in the Anthropic API. Additionally, the function passes a `temperature` parameter to `client.messages.create()`, but the Anthropic API doesn't support the `temperature` parameter (it uses `temperature` in a different context or doesn't support it in this method). This causes the random query generation to fail when using Anthropic as the LLM provider.

## Solution Statement
Fix the Anthropic model references and API call to use the correct current model name (`claude-3-5-sonnet-20241022`) and remove the unsupported `temperature` parameter from the Anthropic API calls. The temperature parameter should be removed from both `generate_random_query_with_anthropic()` and `generate_sql_with_anthropic()` functions since it's not supported by the Anthropic Python SDK in the `messages.create()` method.

## Steps to Reproduce
1. Start the application server and client
2. Upload sample data or a CSV/JSON file to populate the database
3. Click the "Generate Random Query" button
4. When using Anthropic as the LLM provider (if ANTHROPIC_API_KEY is set and OPENAI_API_KEY is not set), the request will fail with an API error about an invalid model or unsupported parameter

## Root Cause Analysis
1. **Invalid Model Name**: The model `"claude-sonnet-4-0"` was intended during a previous feature branch but doesn't exist in the actual Anthropic API. The correct current model is `"claude-3-5-sonnet-20241022"` or another valid Claude model.

2. **Unsupported Parameter**: The Anthropic SDK's `client.messages.create()` method doesn't accept a `temperature` parameter directly. The parameter was added to the random query function (with value 0.8) but also appears in the SQL generation function (with value 0.1). This causes an API validation error.

3. **Location**: Both issues occur in `app/server/core/llm_processor.py`:
   - Line 103 (approx): `generate_sql_with_anthropic()` - has temperature=0.1
   - Line 232 (approx): `generate_random_query_with_anthropic()` - has temperature=0.8
   - Multiple locations: Model name `"claude-sonnet-4-0"` appears 3+ times

## Relevant Files

These files need to be modified to fix the bug:

- **app/server/core/llm_processor.py**
  - Contains `generate_sql_with_anthropic()` function with invalid model and temperature parameter
  - Contains `generate_random_query_with_anthropic()` function with invalid model and temperature parameter
  - The Anthropic API calls use a non-existent model name and unsupported parameters

- **app/server/tests/core/test_llm_processor.py** (if exists)
  - May contain test assertions that reference the old model name and need updating

- **app/client/src/main.ts**
  - Contains the client-side event handler for the "Generate Random Query" button
  - This file doesn't need changes but should work once the backend is fixed

### New Files
None needed

## Step by Step Tasks

### 1. Update Anthropic Model Names in llm_processor.py
- Find all occurrences of `model="claude-sonnet-4-0"` in the file
- Replace with `model="claude-3-5-sonnet-20241022"` (or verify the correct current model name)
- Ensure the change is made in both `generate_sql_with_anthropic()` and `generate_random_query_with_anthropic()` functions
- There are 3 occurrences to fix

### 2. Remove Unsupported Temperature Parameters
- In `generate_sql_with_anthropic()`, remove the line `temperature=0.1,` from the `client.messages.create()` call
- In `generate_random_query_with_anthropic()`, remove the line `temperature=0.8,` from the `client.messages.create()` call
- The Anthropic SDK doesn't support temperature in the messages.create() method in this way

### 3. Update Test Cases (if applicable)
- Check if `app/server/tests/core/test_llm_processor.py` exists
- If it contains test assertions referencing the old model name `"claude-sonnet-4-0"`, update them to use the new model name
- Run the test suite to ensure all tests pass

### 4. Validate the Fix
- Start the server: `cd app/server && uv run python server.py`
- Start the client: `cd app/client && bun run dev`
- Upload sample data to populate the database
- Click the "Generate Random Query" button
- Verify that a random query is generated and displayed in the query input field
- Verify that the generated query is natural language and contextually relevant to the data

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/server && grep -n "claude-sonnet-4-0" core/llm_processor.py` - Verify no invalid model names remain
- `cd app/server && grep -n "temperature=" core/llm_processor.py` - Verify no temperature parameters in Anthropic calls (only OpenAI should have it if needed)
- `cd app/server && uv run pytest` - Run server tests to validate the bug is fixed with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate the bug is fixed with zero regressions
- Manual testing: Upload sample data, click "Generate Random Query" button, verify a query is generated successfully

## Notes

- The issue was introduced in a previous feature upgrade where the model names were changed but the wrong model ID was used
- The feature doc `app_docs/feature-4c768184-model-upgrades.md` references `claude-sonnet-4-0` as the target model, but this model doesn't exist in the actual Anthropic API
- The correct approach is to use the latest available Claude model (e.g., `claude-3-5-sonnet-20241022`)
- When removing temperature parameters, be aware that OpenAI API calls may still use temperature parameters (they're not removed from OpenAI functions)
- Only Anthropic API calls need the temperature parameter removed
