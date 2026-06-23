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

**The game's purpose:** "Glitchy Guesser" is a Streamlit number-guessing game. The app picks a secret number within a range based on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player tries to guess it within a limited number of attempts. After each guess the game gives a "Too High" / "Too Low" hint and updates the score.

**Bugs I found:**
- **You couldn't win on an even-numbered attempt.** On even turns the secret was converted to a string before being compared to the guess, so `42 == "42"` was always `False` — even the exact right number was rejected.
- **The higher/lower hints were backwards.** A guess that was too high told the player to "Go HIGHER!", and the broken string-comparison fallback compared numbers as text (so `"9" > "100"`), pointing players the wrong way.
- **"New Game" left the game frozen.** It only reset the attempts and secret, not the game status/score/history, so after a loss the app stayed stuck on the "Game over" screen and wouldn't let you play again. It also ignored the selected difficulty and always used a 1–100 range.

**Fixes I applied:**
- Removed the `str()` cast so the guess and secret are always compared as integers, and rewrote `check_guess` so the hints point the correct direction (too high → "Go LOWER", too low → "Go HIGHER").
- Made "New Game" reset all session state (attempts, secret, score, status, history) and pick the secret from the current difficulty's range.
- Refactored the game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py`, and added tests that confirm the fixes.

## 📸 Demo Walkthrough

A text-based walkthrough of a sample game on **Normal** difficulty (secret = 50, range 1–100, 8 attempts). The secret is visible in the "Developer Debug Info" panel.

1. The app loads. The player opens **Developer Debug Info** and sees the secret is **50**.
2. The player enters **40** and clicks **Submit Guess** → game returns **"📈 Go HIGHER!"** (Too Low).
3. The player enters **70** → game returns **"📉 Go LOWER!"** (Too High). The hints now point the correct direction.
4. The player enters **60** → **"📉 Go LOWER!"** (Too High). This is an even-numbered attempt, and the guess is still compared correctly (the old bug would have broken here).
5. The score updates after each guess based on the outcome and attempt number.
6. The player enters **50** → game returns **"🎉 Correct!"**, shows balloons, reveals the secret, and displays the final score. The game status becomes "won".
7. The player clicks **New Game 🔁** → all state resets (attempts, score, status, history) and a fresh secret is chosen, so a brand-new game starts immediately instead of freezing.

## 🧪 Test Results

All 6 tests pass — the 3 original starter tests (fixed to unpack the `(outcome, message)` tuple) plus 3 new tests targeting the hint-direction and exact-match-win bugs.

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: ...\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collecting ... collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 50%]
tests/test_game_logic.py::test_too_high_tells_player_to_go_lower PASSED  [ 66%]
tests/test_game_logic.py::test_too_low_tells_player_to_go_higher PASSED  [ 83%]
tests/test_game_logic.py::test_exact_guess_is_a_win PASSED               [100%]

============================== 6 passed in 0.11s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
