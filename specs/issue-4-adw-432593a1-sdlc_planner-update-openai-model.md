# Chore: Support better models for query generation

## Metadata
issue_number: `4`
adw_id: `432593a1`
issue_json: `{"number":4,"title":"Support better models for query generation","body":"chore - adw_sdlc_iso\n\nupdate openai model to use o4-mini (o4-mini-2025-04-16)"}`

## Chore Description
Update the OpenAI model configuration in the Natural Language SQL Interface application to use the newer o4-mini model (specifically `o4-mini-2025-04-16`) for improved query generation. This involves updating the model identifier used in both SQL generation and random query generation functions.

## Relevant Files
Use these files to resolve the chore:

- `app/server/core/llm_processor.py` - Contains the OpenAI model configuration that needs to be updated
  - Line 44: Currently uses `gpt-4.1-2025-04-14` in `generate_sql_with_openai` function
  - Line 184: Currently uses `gpt-4.1-2025-04-14` in `generate_random_query_with_openai` function
  - These need to be changed to `o4-mini-2025-04-16`

- `app/server/tests/core/test_llm_processor.py` - Contains test assertions that verify the model name
  - Line 44: Test assertion expects `gpt-4.1-2025-04-14` model name
  - This needs to be updated to `o4-mini-2025-04-16` to match the new model

- `app_docs/feature-4c768184-model-upgrades.md` - Documentation of previous model upgrades
  - This file documents the previous model upgrade but does not need to be modified for this chore
  - It serves as reference for understanding the model configuration history

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update OpenAI model in SQL generation function
- Open `app/server/core/llm_processor.py`
- Locate the `generate_sql_with_openai` function (around line 7-66)
- Change the model parameter on line 44 from `"gpt-4.1-2025-04-14"` to `"o4-mini-2025-04-16"`
- Verify the change is complete and the syntax is correct

### 2. Update OpenAI model in random query generation function
- In the same file `app/server/core/llm_processor.py`
- Locate the `generate_random_query_with_openai` function (around line 146-197)
- Change the model parameter on line 184 from `"gpt-4.1-2025-04-14"` to `"o4-mini-2025-04-16"`
- Verify the change is complete and the syntax is correct

### 3. Update test assertions for the new model
- Open `app/server/tests/core/test_llm_processor.py`
- Locate the `test_generate_sql_with_openai_success` test function (around line 16-46)
- Change the assertion on line 44 from `'gpt-4.1-2025-04-14'` to `'o4-mini-2025-04-16'`
- Verify the change is complete and the syntax is correct

### 4. Run validation commands
- Execute all commands in the `Validation Commands` section below
- Ensure all tests pass with zero errors
- Verify the model configuration is correctly updated

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `cd app/server && python -c "from core.llm_processor import generate_sql_with_openai, generate_random_query_with_openai; print('Model imports successful')"` - Verify the module imports correctly after changes

## Notes
- This is a straightforward model identifier update similar to the previous upgrade documented in `app_docs/feature-4c768184-model-upgrades.md`
- The o4-mini model should provide better performance for query generation tasks
- No changes to API interfaces, function signatures, or environment variables are required
- The Anthropic model configuration (`claude-sonnet-4-0`) remains unchanged
- All existing functionality and tests should continue to work with the new model identifier
