from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New tests targeting the bug I fixed (backwards higher/lower hint) ---

def test_too_high_tells_player_to_go_lower():
    # BUG FIX: a guess that is too high must tell the player to go LOWER.
    # The original code said "Go HIGHER!" when the guess was already too high.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_too_low_tells_player_to_go_higher():
    # BUG FIX: a guess that is too low must tell the player to go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_exact_guess_is_a_win():
    # BUG FIX: guessing the exact number must always be a win. The old code
    # cast the secret to a string on even attempts, so this could fail.
    outcome, message = check_guess(42, 42)
    assert outcome == "Win"
