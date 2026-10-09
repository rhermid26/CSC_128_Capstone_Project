
import streamlit as st
from agent import run_agent


st.title("Study Buddy")
st.caption("You are chatting with an automated assistant, not a person.")

st.write(
    "Get study tips, understand difficult topics, "
    "and organize your study time."
)


# Store the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get a new question
if prompt := st.chat_input("What do you need help studying?"):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Study Buddy is thinking..."):
                response = run_agent(
                    st.session_state.messages.copy()
                )

            st.write(response)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

        except Exception:
            st.error(
                "Sorry, something went wrong. "
                "Check your API key and try again."
            )