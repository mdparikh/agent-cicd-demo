"""
Simple LLM-as-a-Judge quality gate.

This complements Promptfoo. Promptfoo checks deterministic assertions;
this script demonstrates a model-based aggregate score gate.
"""

import json
import re
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from agent_app import ask_agent, lookup_order, search_faq
from dotenv import load_dotenv
load_dotenv()

THRESHOLD = 8.0

judge_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

CASES = [
    ("Where is my order 1001?", lookup_order.invoke("1001")),
    ("What is the status of order 1003?", lookup_order.invoke("1003")),
    # ("Can I return an item?", search_faq.invoke("return")),
    # ("How long does a refund take?", search_faq.invoke("refund")),
]

def judge(question, facts, answer):
    prompt = f"""
Evaluate this customer support answer.

Return ONLY JSON:
{{
  "correctness": 1-10,
  "relevance": 1-10,
  "faithfulness": 1-10,
  "overall": 1-10,
  "reason": "brief explanation"
}}

QUESTION:
{question}

FACTS:
{facts}

ANSWER:
{answer}
"""
    response = judge_llm.invoke(prompt)
    text = response.content
    if isinstance(text, list):
        text = "".join(
            p.get("text", "") if isinstance(p, dict) else str(p)
            for p in text
        )
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"Judge did not return JSON: {text}")
    return json.loads(match.group())

scores = []

for question, facts in CASES:
    answer = ask_agent(question)
    result = judge(question, facts, answer)
    scores.append(result["overall"])
    print(question)
    print(result)

average = sum(scores) / len(scores)
print(f"\nAverage judge score: {average:.2f}")
print(f"Required threshold: {THRESHOLD:.2f}")

if average < THRESHOLD:
    print("QUALITY GATE FAILED")
    sys.exit(1)

print("QUALITY GATE PASSED")
