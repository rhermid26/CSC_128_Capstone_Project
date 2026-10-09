
from agent import run_agent

messages = [
    {
        "role": "user",
        "content": "Give me three tips for studying Python."
    }
]

print(run_agent(messages))