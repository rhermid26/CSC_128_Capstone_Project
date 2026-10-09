# agent.py
import json
import os
from groq import Groq
from tools import TOOL_SCHEMAS, AVAILABLE_TOOLS, reset_availabilities

client = Groq(api_key=os.environ["GROQ_API_KEY"])

##MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_NAME = "openai/gpt-oss-20b"


def run_agent(messages):
    """Let the model call tools until it produces a final answer."""
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # No tool requested means the model is done
        if not message.tool_calls:
            return message.content

        #messages.append(message.model_dump())

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in message.tool_calls
            ],
        })

        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            if name not in AVAILABLE_TOOLS:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = AVAILABLE_TOOLS[name](**args)
                except Exception as error:
                    result = f"Tool failed: {error}"

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "I was not able to finish that request."