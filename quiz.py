# quiz.py
from dataclasses import dataclass
from typing import Tuple, List

@dataclass(frozen=True)
class Question:
    prompt: str
    options: Tuple[str, ...]
    correct: str

    def is_correct(self, chosen: str) -> bool:
        return chosen == self.correct

class Quiz:
    def __init__(self, questions: List[Question]) -> None:
        self.questions = questions
        self._correct_count = 0

    def run(self) -> None:
        print("\n=== Quiz ===")
        for idx, q in enumerate(self.questions, start=1):
            print(f"\nQ{idx}. {q.prompt}")
            for i, opt in enumerate(q.options, start=1):
                print(f"  {i}) {opt}")

            choice = self._ask_choice(len(q.options))
            chosen_text = q.options[choice - 1]

            if q.is_correct(chosen_text):
                self._correct_count += 1
                print("✅ Correct!")
            else:
                print(f"❌ Wrong. Correct: {q.correct}")

        total = len(self.questions)
        print("\n--- Quiz complete ---")
        print(f"Score: {self._correct_count}/{total} ({(self._correct_count/total)*100:.1f}%)")

    def _ask_choice(self, count: int) -> int:
        while True:
            raw = input("Enter choice number: ").strip()
            if raw.isdigit():
                num = int(raw)
                if 1 <= num <= count:
                    return num
            print(f"Please enter a number between 1 and {count}.")
