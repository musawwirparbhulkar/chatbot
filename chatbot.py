"""
Rule-Based Chatbot
------------------
A simple chatbot that responds to user input using predefined rules and
keyword patterns. Built with basic if-else / pattern-matching logic in
pure Python (no external libraries).

How the chatbot decides what to say:
  1. The user's input is normalized (lowercased + whitespace stripped).
  2. We check for exit commands first so the user can always quit cleanly.
  3. We walk through a list of RULES, in order. Each rule has:
       - "patterns":  a list of regex patterns (any match = rule fires).
       - "responses": a list of possible replies (one is picked at random).
     The FIRST rule whose pattern matches wins, so put more specific
     rules before more general ones.
  4. If no rule matches, we return a random FALLBACK response.
  5. Placeholders like {time}, {date}, and {match} are filled in dynamically
     with real values before the response is shown to the user.

Run it interactively:
    python chatbot.py

Run a quick demo with canned inputs (no typing required):
    python chatbot.py --demo
"""

import re
import random
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------
# Order matters: the first rule whose patterns match wins. We use word
# boundaries (\b) so a pattern like "hi" doesn't accidentally fire on
# words like "history" or "this".
# ---------------------------------------------------------------------------

RULES = [
    # --- Greetings ---------------------------------------------------------
    {
        "patterns": [r"\b(hi|hello|hey|hola|howdy|yo)\b"],
        "responses": [
            "Hey there! How can I help you today?",
            "Hello! What's on your mind?",
            "Hi! Glad you stopped by.",
        ],
    },
    {
        # "Good morning/afternoon/evening" — the captured word becomes {match}.
        "patterns": [r"\bgood\s+(morning|afternoon|evening)\b"],
        "responses": [
            "Good {match} to you too! How's it going?",
            "{match.capitalize()}! Hope your day is going well.",
        ],
    },

    # --- Small talk -------------------------------------------------------
    {
        "patterns": [r"\bhow\s+are\s+you\b", r"\bhow('?s| is) it going\b"],
        "responses": [
            "I'm just code, but I'm running smoothly! How are you?",
            "Doing great -- ready to chat. How about you?",
        ],
    },

    # --- Identity ---------------------------------------------------------
    {
        "patterns": [r"\bwhat('?s| is) your name\b", r"\bwho are you\b"],
        "responses": [
            "I'm a rule-based chatbot. You can call me Bot.",
            "They call me Bot -- a simple pattern-matching assistant.",
        ],
    },

    # --- Help / capabilities ---------------------------------------------
    {
        "patterns": [r"\b(what can you do|help|capabilities)\b"],
        "responses": [
            "I can chat about greetings, answer simple questions, and tell "
            "jokes. Try 'tell me a joke', 'what's the time', or just say hi!",
        ],
    },

    # --- Jokes ------------------------------------------------------------
    {
        "patterns": [r"\b(joke|funny|make me laugh)\b"],
        "responses": [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer I needed a break -- it said 'No problem, I'll go to sleep.'",
        ],
    },

    # --- Time / date ------------------------------------------------------
    {
        "patterns": [r"\b(what('?s| is) the )?time\b", r"\bcurrent time\b"],
        "responses": ["It's {time} right now."],
    },
    {
        "patterns": [r"\b(what('?s| is) the )?date\b", r"\btoday'?s? date\b"],
        "responses": ["Today is {date}."],
    },

    # --- Thanks -----------------------------------------------------------
    {
        "patterns": [r"\b(thanks|thank you|thx|ty)\b"],
        "responses": [
            "You're welcome!",
            "Anytime!",
            "Happy to help!",
        ],
    },

    # --- Goodbye ----------------------------------------------------------
    {
        "patterns": [r"\b(bye|goodbye|see you|quit|exit)\b"],
        "responses": [
            "Goodbye! Talk soon.",
            "See you later!",
        ],
    },
]

# Used when no rule fires — keeps the bot from going silent on weird input.
FALLBACK_RESPONSES = [
    "Hmm, I'm not sure I understand. Try asking for 'help' to see what I can do.",
    "I didn't catch that. Could you rephrase?",
    "I'm only a simple bot -- I might be missing what you mean.",
]


# ---------------------------------------------------------------------------
# Matching + response logic
# ---------------------------------------------------------------------------

def find_match(user_input: str):
    """
    Walk through RULES in order. Return (rule, match_object) for the first
    rule whose any pattern matches the input. Returns (None, None) if no
    rule matches. This is the heart of the rule engine.
    """
    for rule in RULES:
        for pattern in rule["patterns"]:
            match = re.search(pattern, user_input, flags=re.IGNORECASE)
            if match:
                return rule, match
    return None, None


def fill_placeholders(response: str, match) -> str:
    """
    Replace {match}, {time}, and {date} placeholders in a response template
    with real values. `match` is a re.Match object (or None).
    """
    # {match} = whatever the first capturing group of the matched pattern
    # grabbed (e.g. "morning" from "good morning"). Only swap it in if a
    # group was actually captured.
    if match and match.lastindex and match.group(1):
        response = response.replace("{match}", match.group(1))

    now = datetime.now()
    response = response.replace("{time}", now.strftime("%H:%M"))
    response = response.replace("{date}", now.strftime("%Y-%m-%d"))
    return response


def get_response(user_input: str) -> str:
    """
    Top-level decision function. Same flow described in the module docstring:
      1. Normalize input.
      2. Check for exit commands first (so 'quit' always works).
      3. Try to match a rule (first match wins).
      4. Otherwise, return a random fallback response.
    """
    # 1. Normalize — makes matching case- and whitespace-insensitive.
    text = user_input.lower().strip()

    # Empty input gets a nudge instead of falling through to the fallback.
    if not text:
        return "Say something — I'm listening!"

    # 2. Exit commands take priority so the user can always quit.
    if text in {"quit", "exit", "bye", "goodbye"}:
        return "Goodbye!"

    # 3. First matching rule wins.
    rule, match = find_match(text)
    if rule:
        return fill_placeholders(random.choice(rule["responses"]), match)

    # 4. Nothing matched — fall back gracefully.
    return random.choice(FALLBACK_RESPONSES)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def interactive_loop():
    """REPL-style chat loop. Reads from stdin, writes to stdout."""
    print("Bot: Hi! I'm a rule-based chatbot.")
    print("Bot: Type 'help' to see what I can do, or 'quit' to exit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Handles Ctrl+C / Ctrl+D gracefully.
            print("\nBot: Goodbye!")
            break

        if not user:
            continue

        reply = get_response(user)
        print(f"Bot: {reply}\n")

        if reply.startswith("Goodbye"):
            break


def demo():
    """Run the bot against a few canned inputs to show how it behaves."""
    samples = [
        "Hello!",
        "Good morning",
        "How are you?",
        "What's your name?",
        "What can you do?",
        "Tell me a joke",
        "What time is it?",
        "Thank you so much",
        "asdfghjkl",       # unknown input -> fallback
        "bye",
    ]
    print("=== Demo run ===")
    for s in samples:
        print(f"You: {s}")
        print(f"Bot: {get_response(s)}\n")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        interactive_loop()
