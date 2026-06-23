# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the app, it loaded as a "Glitchy Guesser" number-guessing game with a difficulty selector, a guess box, and Submit/New Game buttons. It looked normal at first, but as soon as I started playing it behaved strangely: correct guesses sometimes weren't accepted, the "higher/lower" hints occasionally pointed the wrong way, and clicking "New Game" after a loss didn't actually let me play again.

**Bug 1 — You can't win on an even attempt.** On every even-numbered guess, the secret number is turned into a string before being compared to my guess, so `42 == "42"` is always false. Even typing the exact right number didn't register as a win, and the higher/lower hints were compared as text and pointed the wrong way.

**Bug 2 — "New Game" was broken.** The button only reset the attempts and the secret number but never reset the game's status, so after losing once the game stayed stuck on the "Game over" screen and wouldn't let me start fresh.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess the exact secret on an even attempt (e.g. 2nd guess = 42 when secret is 42) | Game says "Correct!" and I win | Says "Too High"/"Too Low" and never accepts the win; hints point the wrong way | No error; secret is cast to a string so `42 == "42"` is False |
| Lose a game, then click "New Game" | A fresh game starts and I can guess again | Stays stuck on the "Game over" screen and won't let me play | No error; status is never reset to "playing", so `st.stop()` runs |
| Type a non-number like "abc" and click Submit | Show an error and do NOT use up an attempt | Shows "That is not a number." but still burns one attempt | No error; attempts counter is incremented before the guess is validated |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).


**AI tools used:** I used Claude (running as Claude Code inside VS Code in agent mode) to investigate the glitches, refactor the logic, and write tests.

**A correct suggestion:** The AI suggested that the "can't win on an even attempt" glitch came from the secret being cast to a string on even turns (`secret = str(...)`), which makes `42 == "42"` always False, and that removing the cast plus fixing the backwards higher/lower hints in `check_guess` would solve it. This was correct — I verified it two ways: I ran pytest and all 6 tests passed (including a new one asserting that a too-high guess says "Go LOWER"), and I played the live app and won on an even-numbered guess, which used to be impossible.

**An incorrect/misleading suggestion:** At first the AI assumed the existing starter tests would pass alongside my new ones, but that was misleading — those tests compared `check_guess(...)` directly to "Win", even though the function actually returns a tuple `(outcome, message)`, so they were silently failing the whole time. I caught this by actually running pytest instead of trusting the claim, saw the mismatch in the code, and fixed the tests to unpack the tuple (`outcome, message = check_guess(...)`) before they passed. This taught me to verify AI claims by running the code rather than assuming the AI was right.

**A suggestion I rejected:** The AI also listed several extra "bugs" that weren't really broken — like the Hard difficulty having a smaller range than Normal, which is just a design choice, not a defect. I rejected those because I couldn't reproduce any actual broken behavior when I played the game, and I only kept the bugs I could confirm with my own testing. This kept me in control of the process instead of blindly trusting the AI's full list.


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?


**How I decided a bug was really fixed:** I decided a bug was fixed only when I could confirm it two ways: an automated test passing and the correct behavior showing up in the live game. I didn't trust a fix just because the code "looked right" — I reproduced the original bug first, applied the fix, and then checked that the broken behavior was actually gone.

**A test I ran:** I ran pytest and wrote a test called `test_too_high_tells_player_to_go_lower`, which checks that guessing 60 against a secret of 50 returns "Too High" and a message containing "LOWER". This showed me that my `check_guess` fix worked, and it also surfaced something I didn't expect — the starter tests were comparing the result directly to "Win" even though `check_guess` returns a tuple `(outcome, message)`, so those tests had actually been failing. After fixing them to unpack the tuple, all 6 tests passed. I also tested manually by opening the Developer Debug Info, reading the secret, and winning on an even-numbered guess — which used to be impossible before the fix.

**Did AI help with tests:** Yes — the AI helped me write tests that targeted the specific bug instead of just testing random inputs, like asserting the direction of the hint ("LOWER"/"HIGHER") rather than only the outcome string. It also explained why the starter tests were failing (the tuple-vs-string mismatch), which helped me understand that a test passing or failing depends on matching the function's real return type, not just the value I expected.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

The way I'd explain it to a friend: every time you interact with a Streamlit app  click a button, type in a box, change a dropdown, Streamlit doesn't just update one piece, it re-runs the entire app.py file from the top to the bottom again. So you can't rely on a normal variable to "remember" anything, because every variable gets recreated from scratch on each rerun. That's what st.session_state is for: it's like a small backpack the app carries between reruns, holding things you want to keep — the secret number, the score, how many attempts you've used, and the game's status.

This project made that click for me because of the "New Game" bug. The button was resetting the secret and attempts, but it never reset status back to "playing", so on the very next rerun the app read status == "lost" from the backpack and immediately hit st.stop(), freezing on the "Game over" screen. The fix wasn't about the button logic itself — it was realizing that the button only changes session state, and then a fresh rerun reads that state and decides what to show. Once I understood that the script runs top-to-bottom every time and that session state is the only thing that survives, the bug made total sense: if you don't reset a value in the backpack, the next rerun keeps acting on the old one.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


**A habit I want to reuse:** The biggest one is writing a test that reproduces the bug first, before I trust that a fix worked. On this project I confirmed every fix two ways — a passing pytest test and the correct behavior in the live game — instead of assuming the code was right because it looked right. I want to keep this "verify, don't trust" habit, because it's what caught the starter tests that were secretly failing the whole time.

**One thing I'd do differently:** I'd verify the AI's claims earlier instead of taking them at face value. The AI assumed the existing tests would pass, and I only found out they were broken once I actually ran pytest — next time I'll run the tests and the app first to see the real starting state before letting the AI make changes on top of assumptions.

**How this changed how I think about AI-generated code:** It showed me that AI can be a fast and genuinely helpful teammate for finding and explaining bugs, but its output is a draft to be tested, not a finished answer to be trusted — the code that "claims to be production-ready" is exactly the code you need to verify yourself.