from utils import call_gemini


def build_quiz_prompt(notes):
    return f"""You are a university professor creating a quiz.

Based on the following study notes, generate exactly
3 multiple choice questions.

Use this exact format:

Q1: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [letter]
Explanation: [one sentence]

Q2: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [letter]
Explanation: [one sentence]

Q3: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [letter]
Explanation: [one sentence]

Notes:
{notes}"""


def generate_quiz(notes):
    result = call_gemini(build_quiz_prompt(notes))

    if result is None:
        return "Quiz generation failed. Please try again."

    return result