import os
import streamlit as st
from openai import OpenAI

# ✅ Fetch API key from environment variable (Streamlit Secrets or local .env)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment or Streamlit Secrets.")
    st.stop()

# Initialize client
client = OpenAI(api_key=api_key)

st.title("OSS Compliance Chatbot 💬")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask me about OSS compliance:")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )

    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

for msg in st.session_state["messages"]:
    st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
