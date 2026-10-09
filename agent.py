
import json
import os

import streamlit as st
from groq import Groq

from classifier import IntentClassifier
from retriever import Retriever
from tools import TOOL_SCHEMAS, AVAILABLE_TOOLS


MODEL_NAME = "openai/gpt-oss-20b"


# Get the API key from the environment or Streamlit secrets
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        raise RuntimeError(
            "GROQ_API_KEY was not found. Check your environment "
            "variables or Streamlit secrets."
        )

client = Groq(api_key=api_key)


# Create the classifier and retriever
classifier = IntentClassifier()
retriever = Retriever()


SYSTEM_PROMPT = """
You are Study Buddy, a helpful chatbot for students.

Help students understand school subjects, improve study habits,
organize study time, and prepare for tests.

Use simple words and explain difficult topics step by step.
Adapt your advice to the student's question and needs.

Use Python tools when a task needs an exact calculation,
course number format check, or study schedule.

Use retrieved study information when it is relevant.
Do not claim that retrieved information supports something
unless it actually does.

If you do not know something, be honest.
Do not invent school policies, grades, or course information.
You can provide general study advice when no stored information
matches the question, but do not pretend it came from a source.
"""


def run_agent(messages):
    """Classify the question, retrieve information, and call Groq."""

    # Find the latest student question
    question = ""

    for message in reversed(messages):
        if message["role"] == "user":
            question = message["content"]
            break

    if not question:
        return "Please ask me a study-related question."

    # Identify the type of request
    intent, confidence = classifier.classify(question)

    # Find related study information
    hits = retriever.search(question)
    context = retriever.build_context(hits)

    # Give the model useful information about this request
    extra_context = f"Detected request type: {intent or 'unknown'}."

    if intent:
        extra_context += f" Classifier similarity: {confidence:.2f}."

    if context:
        extra_context += "\n\nRetrieved study information:\n" + context
    else:
        extra_context += "\n\nNo matching study information was found."

    # Build the conversation
    agent_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": extra_context},
        *messages
    ]

    # Allow the model to call tools when needed
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=agent_messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # Return the final answer when no tool is requested
        if not message.tool_calls:
            return message.content or "I couldn't generate a response. Please try again."

        # Add the assistant's tool request to the conversation
        agent_messages.append({
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

        # Run each requested Python tool
        for call in message.tool_calls:
            name = call.function.name

            try:
                args = json.loads(call.function.arguments)

                if name not in AVAILABLE_TOOLS:
                    result = f"Unknown tool: {name}"
                else:
                    result = AVAILABLE_TOOLS[name](**args)

            except Exception:
                result = "The tool could not complete that request. Check the provided information."

            agent_messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "I was not able to finish that request. Please try again."