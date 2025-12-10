# main.py
"""
Minimal terminal quiz:
- Fetch 10 questions from Open Trivia DB (API GET + JSON parsing).
- Build Question objects.
- Run quiz and print score.
"""

import json
import random
import sys
import urllib.request
import urllib.error
from html import unescape  # just to display text nicely

from quiz import Question, Quiz

API_URL = "https://opentdb.com/api.php?amount=10"

def fetch_questions():
    print("Contacting API...", flush=True)
    try:
        with urllib.request.urlopen(API_URL, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code}", flush=True)
        return None
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", flush=True)
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Failed to parse API response: {e}", flush=True)
        return None

    if not isinstance(data, dict) or data.get("response_code") != 0:
        print("API returned no results or an unexpected response.", flush=True)
        return None

    results = data.get("results", [])
    if not isinstance(results, list) or not results:
        print("No questions received.", flush=True)
        return None

    print(f"Got {len(results)} questions.", flush=True)
    return results

def make_question(item: dict) -> Question:
    prompt = unescape(item.get("question", "").strip())
    correct = unescape(item.get("correct_answer", "").strip())
    incorrect = [unescape(x.strip()) for x in item.get("incorrect_answers", [])]

    if item.get("type") == "boolean":
        options = ["True", "False"]
        if correct not in options:
            correct = "True" if correct.lower() == "true" else "False"
    else:
        options = incorrect + [correct]
        options = list(dict.fromkeys(options))
        random.shuffle(options)

    return Question(prompt=prompt, options=tuple(options), correct=correct)

def main():
    print("=== Quiz App (Open Trivia DB) ===", flush=True)
    print("Fetching questions...", flush=True)
    items = fetch_questions()
    if items is None:
        input("\nPress Enter to exit...")
        return

    questions = [make_question(it) for it in items]
    quiz = Quiz(questions)
    quiz.run()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
