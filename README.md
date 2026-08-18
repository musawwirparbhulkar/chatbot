# Rule-Based Chatbot

A simple Python chatbot that replies to user input using predefined rules and
keyword patterns. Built with basic if-else / pattern-matching logic and zero
external dependencies.

This is the first internship task: a minimal conversational agent that
handles greetings, common small-talk questions, and a graceful fallback
when it doesn't understand the input.

---

## Features

- Greeting detection: `hi`, `hello`, `hey`, `hola`, `howdy`, `yo`,
  plus time-of-day greetings (`good morning`, etc.)
- Small talk: `how are you`, `what's your name`, `who are you`
- Help / capabilities menu
- A couple of jokes on demand
- Live time and date responses
- Thanks + goodbye handling
- Fallback reply for anything it doesn't recognize

---

## Requirements

- Python 3.8 or newer (uses f-strings and the `re` module from the standard
  library; nothing to install).

Verify your Python version:

```powershell
python --version
```

---

## How to Run

From the project folder:

```powershell
cd "C:\Users\Admin\.minimax-agent\projects\rule-based-chatbot"
```

### Interactive mode (chat with the bot)

```powershell
python chatbot.py
```

You'll see a prompt. Type messages and press Enter. Type `quit`, `exit`,
or `bye` to end the session.

### Demo mode (canned test inputs, no typing)

```powershell
python chatbot.py --demo
```

Runs 10 pre-written inputs (greetings, time, joke, fallback, etc.) so you
can quickly confirm every rule fires correctly.

### If `python` is not recognized on Windows

```powershell
py chatbot.py --demo
```

The `py` launcher is the official Windows shortcut and works even when
`python` isn't on `PATH`.

---

## Project Structure

```
rule-based-chatbot/
|-- chatbot.py      # All the logic -- rules, matcher, and CLI loop
|-- README.md       # This file
```

Single-file design on purpose: easy to read top-to-bottom in a code review.

---

## How It Works

The decision pipeline is intentionally simple so it's easy to explain:

1. **Normalize** the input -- `lower()` and `strip()` so casing and stray
   whitespace don't break matches.
2. **Exit check** -- `quit`, `exit`, `bye`, and `goodbye` short-circuit
   immediately so the user can always leave.
3. **Walk the rule list in order.** Each rule has:
   - `patterns`  -- a list of regex patterns (any match fires the rule).
   - `responses` -- a list of possible replies (one is picked at random).
   The **first** rule whose pattern matches wins, so more specific rules
   come before more general ones.
4. **Fallback** -- if no rule matches, return a random "I didn't catch
   that" response. The bot never goes silent.
5. **Placeholders** -- templates can include `{time}`, `{date}`, and
   `{match}` (the captured keyword). These are replaced with real values
   before the reply is shown.

Patterns use word boundaries (`\b`) so a keyword like `hi` doesn't
accidentally fire on words like `history` or `this`.

---

## Sample Conversation

```
You: hello
Bot: Hello! What's on your mind?

You: how are you
Bot: I'm just code, but I'm running smoothly! How are you?

You: tell me a joke
Bot: Why don't scientists trust atoms? Because they make up everything!

You: what time is it
Bot: It's 14:18 right now.

You: thanks
Bot: Anytime!

You: asdfghjkl
Bot: I didn't catch that. Could you rephrase?

You: bye
Bot: Goodbye!
```

---

## Extending the Bot

Adding a new rule is a 4-line change inside the `RULES` list in
`chatbot.py`:

```python
{
    "patterns":  [r"\b(weather|forecast)\b"],
    "responses": [
        "I don't have weather data, but you can check a weather app!",
        "Sorry, I can't look outside for you. Try a forecast site?",
    ],
},
```

Rules are checked top-to-bottom, so insert new entries **above** any
catch-all that might shadow them. After editing, run
`python chatbot.py --demo` (or just append your test phrase to the
`samples` list in `demo()`) to confirm the new rule fires.

---

## Notes for the Reviewer

- No external libraries -- only `re`, `random`, `sys`, and `datetime`
  from the Python standard library.
- No persistent state; the bot forgets the conversation between turns
  (a deliberate simplification for this first task).
- ASCII-only output so the bot works cleanly on legacy Windows terminals
  without encoding errors.
