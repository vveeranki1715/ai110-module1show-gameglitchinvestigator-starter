from logic_utils import check_guess, get_hint_message, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- New tests targeting the bugs we fixed ---

def test_hint_message_not_backwards():
    # FIX verification: a "Too High" guess must tell the player to go LOWER,
    # and a "Too Low" guess must tell the player to go HIGHER.
    assert "LOWER" in get_hint_message(check_guess(60, 50))
    assert "HIGHER" in get_hint_message(check_guess(40, 50))

def test_check_guess_handles_string_secret():
    # FIX verification: comparing an int guess to a str secret must not raise
    # a TypeError and must still give the correct outcome.
    assert check_guess(40, "50") == "Too Low"
    assert check_guess(60, "50") == "Too High"

def test_score_never_goes_negative():
    # FIX verification: repeated wrong guesses floor the score at 0.
    score = 0
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt)
    assert score == 0


# --- Challenge 1: Advanced edge-case tests ---

from logic_utils import parse_guess

def test_negative_number_is_handled_gracefully():
    # Edge case: a negative guess should still parse and compare (Too Low vs 50).
    ok, value, err = parse_guess("-5")
    assert ok and value == -5 and err is None
    assert check_guess(value, 50) == "Too Low"

def test_decimal_input_is_truncated():
    # Edge case: a decimal like "40.9" should truncate to int 40, not crash.
    ok, value, err = parse_guess("40.9")
    assert ok and value == 40
    assert check_guess(value, 50) == "Too Low"

def test_extremely_large_value_does_not_overflow():
    # Edge case: a huge number should parse and compare without error/overflow.
    ok, value, err = parse_guess("1000000000000")
    assert ok and value == 1000000000000
    assert check_guess(value, 50) == "Too High"

def test_non_numeric_input_is_rejected():
    # Edge case: garbage text returns a friendly error instead of raising.
    ok, value, err = parse_guess("abc")
    assert not ok and value is None and err == "That is not a number."

def test_empty_input_is_rejected():
    # Edge case: empty string prompts the user to enter a guess.
    ok, value, err = parse_guess("")
    assert not ok and err == "Enter a guess."
