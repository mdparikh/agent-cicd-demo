import json
import sys
from agent_app import ask_agent

# request = json.load(sys.stdin)
# question = request.get("prompt", "")

# sys.argv[1] contains the rendered {{question}} prompt
question = sys.argv[1]
answer = ask_agent(question)

print(json.dumps({"output": answer}))
