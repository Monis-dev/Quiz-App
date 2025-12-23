import json
import random
import urllib.request
from html import unescape

API_URL = "https://opentdb.com/api.php?amount=10"

def get_questions():
    with urllib.request.urlopen(API_URL, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("response_code") != 0:
        return []
    return data["results"]

def make_q(item):
    prompt = unescape(item.get("question", ""))
    correct = unescape(item.get("correct_answer", ""))
    incorrect = [unescape(x) for x in item.get("incorrect_answers", [])]

    if item.get("type") == "boolean":
        options = ["True", "False"]
        correct = "True" if correct.lower() == "true" else "False"
    else:
        options = incorrect + [correct]
        options = list(dict.fromkeys(options))
        random.shuffle(options)
    return prompt, options, correct

def ask(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}) {opt}")
    while True:
        n = input("Enter choice number: ").strip()
        if n.isdigit() and 1 <= int(n) <= len(options):
            return options[int(n) - 1]
        print(f"Please enter 1..{len(options)}")

def main():
    print("Fetching questions...")
    try:
        items = get_questions()
    except Exception as e:
        print("Could not fetch questions:", e)
        return
    if not items:
        print("No questions. Try again later.")
        return

    score = 0
    for idx, it in enumerate(items, 1):
        print(f"\nQ{idx}. ", end="")
        prompt, options, correct = make_q(it)
        choice = ask(prompt, options)
        if choice == correct:
            score += 1
            print("Correct")
        elif (choice == "exit"):
            break
        else:
            print(f"Wrong (correct: {correct})")

    total = len(items)
    print("\n--- Done ---")
    print(f"Score: {score}/{total} ({(score/total)*100:.1f}%)")

if __name__ == "__main__":
    main()
