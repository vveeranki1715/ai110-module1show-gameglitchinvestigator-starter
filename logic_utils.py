# FIX: Refactored core game logic out of app.py into this module with the help
# of my AI coding assistant (agent mode). The AI moved the four functions here,
# fixed the inverted high/low hint bug and the negative-score bug, and I
# reviewed every diff before accepting it.

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: Force both values to int so an int-vs-str comparison can never raise
    # a TypeError (the old code cast the secret to str on even attempts).
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


# FIX: Hint text now matches the outcome. The original code paired "Too High"
# with "Go HIGHER!" (and "Too Low" with "Go LOWER!"), which was backwards.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_hint_message(outcome: str):
    """Return the user-facing hint for a given outcome."""
    return HINT_MESSAGES.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number. Never goes below 0."""
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        # FIX: Floor the score at 0 so wrong guesses can't produce a negative score.
        return max(0, current_score - 5)

    return current_score
