# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app via Streamlit, the game looked fine on the surface — a title, a difficulty selector, an input box, and a "Submit Guess" button. But as soon as I started playing, the hints made no sense. No matter what number I guessed, it almost always told me to "Go LOWER," even when I guessed `1` and the debug panel showed the secret was much higher than my guess. After running out of attempts I got a "wrong" message and, oddly, a **negative score**.

Concrete bugs I noticed:

- **Backwards hints (inverted feedback).** In `check_guess`, the outcome labels are paired with the wrong messages. When the guess is *higher* than the secret it returns the "Go HIGHER!" message, and when the guess is *lower* than the secret it returns "Go LOWER!" — both are reversed. This is why guessing `1` (below the secret) told me to go lower.
- **Score can go negative.** `update_score` subtracts 5 points for "Too Low" guesses (and on odd attempts for "Too High" too) with no floor at zero, so several wrong guesses drive the score below 0 and I finish with a negative final score.
- **Type-coercion glitch on even attempts.** On every even-numbered attempt, `app.py` converts the secret to a string (`secret = str(st.session_state.secret)`) before calling `check_guess`. Comparing an `int` guess to a `str` secret raises a `TypeError`, which the `except` block silently catches and falls back to comparing them as *strings*. String comparison gives nonsensical results (e.g. `"9" > "50"` is `True`), so hints become inconsistent depending on whether the attempt number is odd or even.
- **(Bonus) Off-by-one "attempts left" + wrong range text.** Attempts start at `1` instead of `0`, so the "Attempts left" counter is off by one, and the info banner always says "between 1 and 100" even on Easy (1–20) or Hard (1–50).

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `1` when secret is `73` (odd attempt) | "Too Low" → hint "Go HIGHER!" | Hint shown was "📉 Go LOWER!" (reversed) | none |
| Guess `90` when secret is `73` (odd attempt) | "Too High" → hint "Go LOWER!" | Hint shown was "📈 Go HIGHER!" (reversed) | none |
| Guess `9` when secret is `50` on an even attempt | "Too Low" (9 < 50) → go higher | Compared as strings `"9" > "50"` → wrong/inconsistent hint | `TypeError: '>' not supported between 'int' and 'str'` (caught silently in `check_guess`) |
| Six wrong guesses in a row | Score floored at 0, never negative | Final score displayed as a negative number (e.g. `-25`) | none |

---

## 2. How did you use AI as a teammate?

I used my AI coding assistant inside VS Code, attaching both `app.py` and `logic_utils.py` so it could see how the UI and logic files related. I started a separate chat per bug and dropped `# FIXME` comments at the "crime scenes" so the AI knew exactly where to look. I then used agent mode to refactor the four functions out of `app.py` into `logic_utils.py` in one multi-step instruction.

**A correct suggestion:** When I asked it to explain why guessing `1` told me to "Go LOWER," the AI pointed out that in `check_guess` the outcome labels were paired with the *opposite* hint messages ("Too High" → "Go HIGHER!"). It suggested separating the comparison from the hint text by using a `HINT_MESSAGES` lookup so the mapping is obvious and can't drift. I verified this two ways: in the game, guessing `1` against a secret of `73` now shows "📈 Go HIGHER!"; and `test_hint_message_not_backwards` asserts "LOWER"/"HIGHER" appear for the right outcomes and passes.

**An incorrect/misleading suggestion:** For the even-attempt `str(secret)` glitch, the AI first suggested just wrapping the comparison in a bigger `try/except` to "swallow the TypeError." That was misleading — it would have hidden the bug instead of fixing the behavior, and string comparison (`"9" > "50"`) would still give wrong hints. I caught this by reasoning through the example and by writing `test_check_guess_handles_string_secret`, which only passes once `check_guess` coerces both values to `int`. I rejected the try/except idea and used the int-coercion fix instead.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I had both an automated test proving the logic and a manual playthrough confirming the behavior in the live app. I added three new pytest cases in `tests/test_game_logic.py`: `test_hint_message_not_backwards` (hints point the right way), `test_check_guess_handles_string_secret` (int-vs-str comparison no longer raises and returns the right outcome), and `test_score_never_goes_negative` (repeated wrong guesses floor at 0). Running `pytest` showed `6 passed` — the three original starter tests plus my three new ones.

The string-secret test was the most useful: it failed with a `TypeError` until I coerced both arguments to `int` inside `check_guess`, which proved the real fix had to live in the logic, not in a `try/except`. The AI helped me design the tests by suggesting the secret/guess pairs to use (e.g. guess `60` vs secret `50` for "Too High"), but I chose the edge cases (string secret, score floor) myself based on the actual bugs. Finally I ran `streamlit run app.py` and confirmed that guessing below the secret now says "Go HIGHER!" and the final score never goes negative.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
