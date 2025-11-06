# Chore: Update OpenAI Model to use o4-mini

## Metadata
issue_number: `19`
adw_id: `12f6c576`
issue_json: `{"number":19,"title":"update openai model to use o4-mini","body":"chore - adw_sdlc_iso\n\nupdate openai model to use o4-mini (o4-mini-2025-04-16)\n\n"}`

## Chore Description
Update the OpenAI model configuration throughout the codebase from the current mix of `o4-mini-2025-04-16` and `gpt-4.1-2025-04-14` models to consistently use `o4-mini-2025-04-16` across all LLM processing functions. This includes SQL generation, random query generation, and synthetic data generation functions.

Currently, the codebase has:
- SQL generation functions using `o4-mini-2025-04-16` (already updated)
- Synthetic data generation still using `gpt-4.1-2025-04-14`
- Hook utility script using `gpt-4.1-nano`
- Tests expecting different model names in different functions

This chore will standardize all OpenAI API calls to use `o4-mini-2025-04-16`.

## Relevant Files
Use these files to resolve the chore:

- **app/server/core/llm_processor.py** (lines 45, 184, 346)
  - Contains OpenAI model configuration for SQL generation and synthetic data generation
  - SQL generation functions already use `o4-mini-2025-04-16` (lines 45, 184)
  - Synthetic data generation function uses `gpt-4.1-2025-04-14` (line 346) - needs update

- **app/server/tests/core/test_llm_processor.py** (line 44)
  - Tests verify the model name used in OpenAI API calls
  - Currently expects `o4-mini-2025-04-16` for SQL generation tests
  - Tests are already correct for SQL generation functions

- **app/server/tests/test_data_generation.py** (line 63)
  - Tests for synthetic data generation
  - Currently expects `gpt-4.1-2025-04-14` - needs update to `o4-mini-2025-04-16`
  - Tests verify model configuration for data generation functions

- **.claude/hooks/utils/llm/oai.py** (line 37)
  - Hook utility for OpenAI LLM prompting
  - Currently uses `gpt-4.1-nano` - needs update to `o4-mini-2025-04-16` for consistency

- **app_docs/feature-4c768184-model-upgrades.md**
  - Documentation of previous model upgrades
  - Should be referenced to understand the model upgrade pattern
  - Will need a new documentation file created for this o4-mini upgrade

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update Synthetic Data Generation Model in llm_processor.py
- Open `app/server/core/llm_processor.py`
- Locate the `generate_synthetic_data_with_openai` function (around line 346)
- Change the model from `gpt-4.1-2025-04-14` to `o4-mini-2025-04-16`
- Verify no other OpenAI model references need updating in this file

### Step 2: Update Hook Utility Script Model
- Open `.claude/hooks/utils/llm/oai.py`
- Locate the `prompt_llm` function (around line 37)
- Change the model from `gpt-4.1-nano` to `o4-mini-2025-04-16`
- This ensures consistency across all OpenAI API calls in the codebase

### Step 3: Update Synthetic Data Generation Test Expectations
- Open `app/server/tests/test_data_generation.py`
- Locate the test assertion for model name (line 63)
- Change the expected model from `gpt-4.1-2025-04-14` to `o4-mini-2025-04-16`
- This aligns the test expectations with the updated implementation

### Step 4: Verify SQL Generation Tests Are Correct
- Open `app/server/tests/core/test_llm_processor.py`
- Verify line 44 correctly expects `o4-mini-2025-04-16` for SQL generation
- No changes needed here - tests are already correct for SQL generation functions

### Step 5: Run Validation Commands
- Execute all validation commands to ensure the chore is complete with zero regressions
- All tests must pass without errors

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Verify SQL generation tests pass with correct model
- `cd app/server && uv run pytest tests/test_data_generation.py -v` - Verify synthetic data generation tests pass with updated model
- `cd app/server && uv run pytest` - Run all server tests to validate zero regressions across the entire codebase

## Notes
- The o4-mini model (o4-mini-2025-04-16) is OpenAI's latest efficient model suitable for SQL generation and data synthesis tasks
- This update maintains backward compatibility as it's only changing the model identifier, not the API interface
- The previous model upgrade documentation in `app_docs/feature-4c768184-model-upgrades.md` shows the pattern for model updates
- SQL generation functions have already been updated to use o4-mini in previous commits (see git status showing recent commit "ce7a09a Remove temperature parameter from o4-mini model calls")
- This chore completes the model migration by updating the remaining synthetic data generation function and hook utility
- All OpenAI API parameter usage should remain consistent with o4-mini requirements (e.g., using `max_completion_tokens` instead of `max_tokens`)
