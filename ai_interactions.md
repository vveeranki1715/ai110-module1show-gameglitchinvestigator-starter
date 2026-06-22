# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompts used:**

```
"Look at parse_guess and check_guess in logic_utils.py. Identify three edge-case
inputs (e.g. negative numbers, decimals, extremely large values) that could still
break the game, and generate a pytest suite that verifies each one is handled
gracefully without raising."
```

```
"Also add edge cases for clearly invalid input — non-numeric text and an empty
string — and assert the exact error message instead of just that it failed."
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative number (`-5`) | Prompt 1 | `test_negative_number_is_handled_gracefully` | ✅ | A `-` sign could break naive parsing; confirms negatives parse and compare correctly. |
| Decimal (`40.9`) | Prompt 1 | `test_decimal_input_is_truncated` | ✅ | Users may type decimals; verifies they truncate to an int instead of crashing. |
| Extremely large value (`1000000000000`) | Prompt 1 | `test_extremely_large_value_does_not_overflow` | ✅ | Huge inputs overflow in some languages; confirms Python ints handle it with no error. |
| Non-numeric text (`abc`) | Prompt 2 | `test_non_numeric_input_is_rejected` | ✅ | Garbage input must return a friendly error, not raise; locks the exact message. |
| Empty string (`""`) | Prompt 2 | `test_empty_input_is_rejected` | ✅ | Submitting nothing should prompt "Enter a guess."; distinguishes "empty" from "invalid". |

All five edge-case tests pass (`11 passed` total). The AI's suggested test bodies were correct; I verified each by running `pytest -v` and by manually tracing the inputs through `parse_guess`/`check_guess`.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
