import os
from openai import OpenAI
import streamlit as st

# ====== Hugging Face Inference Setup ======
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# ====== Streamlit Page Setup ======
st.set_page_config(page_title="OSS Compliance Chatbot 💬", page_icon="💬", layout="centered")
st.title("OSS Compliance Chatbot 💬")
st.write("Ask me about OSS compliance — powered by Meta-LLaMA-3!")

# ====== Initialize Chat History ======
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 How can I help you with OSS compliance today?"}
    ]

# ====== Display Chat Messages ======
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ====== Chat Input Box ======
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate response from the model
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=st.session_state.messages,
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.write(reply)
            except Exception as e:
                st.error(f"❌ Error: {e}")
