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
