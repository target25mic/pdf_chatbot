import sys, json
sys.path.append("backend")
from retrieval import retrieve_relevant_chunks
from generation import generate_answer
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
judge_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def judge_answer(question, expected, actual):
    prompt = f"""Question: {question}
Expected answer: {expected}
Actual answer: {actual}

Does the actual answer correctly convey the expected answer's meaning? Reply with only "CORRECT" or "INCORRECT"."""
    response = judge_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

with open("eval_set.json") as f:
    eval_set = json.load(f)

correct = 0
for item in eval_set:
    chunks = retrieve_relevant_chunks(item["question"])
    answer = generate_answer(item["question"], chunks)
    verdict = judge_answer(item["question"], item["expected_answer"], answer)
    is_correct = "CORRECT" in verdict.upper()
    correct += is_correct
    print(f"Q: {item['question']}\nA: {answer}\nVerdict: {verdict}\n---")

print(f"\nAccuracy: {correct}/{len(eval_set)} = {correct/len(eval_set)*100:.1f}%")