import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agents.clarification_agent import get_clarifying_questions
from agents.reconstruction_agent import reconstruct_prompt
from agents.response_agent import generate_response

def run_pipeline(user_prompt: str) -> dict:
    print("\n📥 Original prompt:", user_prompt)

    print("\n🤔 Generating clarifying questions...")
    questions = get_clarifying_questions(user_prompt)
    print(questions)

    print("\n✏️  Your answers (type each answer and press Enter):")
    answers = []
    for i, line in enumerate(questions.strip().split("\n")):
        if line.strip():
            answer = input(f"  → {line.strip()} \n  Your answer: ")
            answers.append(f"Q: {line.strip()}\nA: {answer}")

    answers_text = "\n\n".join(answers)

    print("\n🔧 Reconstructing prompt...")
    reconstructed = reconstruct_prompt(user_prompt, questions, answers_text)
    print("\n📝 Reconstructed prompt:")
    print(reconstructed)

    print("\n🚀 Generating final response...")
    response = generate_response(reconstructed)
    print("\n✅ Final response:")
    print(response)

    return {
        "original": user_prompt,
        "questions": questions,
        "answers": answers_text,
        "reconstructed": reconstructed,
        "response": response
    }

if __name__ == "__main__":
    vague_prompt = input("Enter your prompt: ")
    run_pipeline(vague_prompt)