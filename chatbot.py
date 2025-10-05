# chatbot.py
import streamlit as st
from openai import OpenAI
import ssl
import certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


# Initialize client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.title("OSS Compliance Chatbot 💬")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# User input
user_input = st.text_input("Ask me about OSS compliance:")

if st.button("Send") and user_input:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Get response
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Or gpt-4o
        messages=st.session_state["messages"]
    )

    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

# Display chat
for msg in st.session_state["messages"]:
    st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
