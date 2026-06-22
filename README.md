# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Purpose of the game.** A Streamlit number-guessing game: the app picks a secret number within a range based on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player has a limited number of attempts to guess it. After each guess the game gives a "higher/lower" hint and updates a score.

- [x] **Bugs I found.**
  1. **Backwards hints** — `check_guess` paired "Too High" with "Go HIGHER!" and "Too Low" with "Go LOWER!", so the hints always pointed the wrong way (guessing `1` below the secret told me to "Go LOWER").
  2. **TypeError / inconsistent hints on even attempts** — `app.py` cast the secret to a string on every even attempt, so comparing an `int` guess to a `str` secret raised a `TypeError` that was silently caught and fell back to string comparison (`"9" > "50"`), giving nonsensical hints.
  3. **Negative score** — `update_score` subtracted points for wrong guesses with no floor, producing a negative final score.
  4. *(bonus)* Off-by-one "attempts left" counter and a hard-coded "between 1 and 100" banner that ignored the difficulty range.

- [x] **Fixes I applied.**
  - Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into `logic_utils.py`.
  - Made `check_guess` return just the outcome and moved hint text into a `HINT_MESSAGES` lookup so the message can never drift from the outcome.
  - Coerced both arguments to `int` inside `check_guess` so an int-vs-str comparison can't raise or fall back to string compare.
  - Floored the score at `0` in `update_score`.
  - Fixed the attempts counter (start at `0`), showed the real difficulty range, and made "New Game" reset all state.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (secret = 73, visible in the Developer Debug Info panel):

1. User enters a guess of **40** → game returns **"Too Low"** with the hint **"📈 Go HIGHER!"**
2. User enters a guess of **90** → game returns **"Too High"** with the hint **"📉 Go LOWER!"**
3. User enters a guess of **70** → **"Too Low" → "📈 Go HIGHER!"**; the score decreases for each wrong guess but never drops below 0.
4. The "Attempts left" counter decreases correctly by one after each submission, and the score updates after every guess.
5. User enters **73** → game shows **"🎉 Correct!"**, triggers balloons, reveals the secret, displays the final score, and sets the status to "won".
6. Clicking **"New Game 🔁"** resets the secret, attempts, score, status, and history so a fresh round starts cleanly.

**Screenshot** *(optional)*: not included — see the text walkthrough above.

## 🧪 Test Results

Includes the **Challenge 1** advanced edge-case suite (negative numbers, decimals, extremely large values, non-numeric and empty input):

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
collected 11 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  9%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 18%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 27%]
tests/test_game_logic.py::test_hint_message_not_backwards PASSED         [ 36%]
tests/test_game_logic.py::test_check_guess_handles_string_secret PASSED  [ 45%]
tests/test_game_logic.py::test_score_never_goes_negative PASSED          [ 54%]
tests/test_game_logic.py::test_negative_number_is_handled_gracefully PASSED [ 63%]
tests/test_game_logic.py::test_decimal_input_is_truncated PASSED         [ 72%]
tests/test_game_logic.py::test_extremely_large_value_does_not_overflow PASSED [ 81%]
tests/test_game_logic.py::test_non_numeric_input_is_rejected PASSED      [ 90%]
tests/test_game_logic.py::test_empty_input_is_rejected PASSED            [100%]

============================== 11 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
