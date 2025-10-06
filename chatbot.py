import os
from openai import OpenAI
import streamlit as st

# ====== Hugging Face Inference Configuration ======
HF_TOKEN = os.getenv("HF_TOKEN")  # from Streamlit Secrets

# Initialize OpenAI client but point to Hugging Face
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# ====== Streamlit UI ======
st.set_page_config(page_title="OSS Compliance Chatbot 💬", page_icon="💬")
st.title("OSS Compliance Chatbot 💬")
st.write("Ask me about OSS compliance:")

user_input = st.text_input("Your question:")

# ====== Chat Logic ======
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = client.chat.completions.create(
                    model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",  # ✅ uses Hugging Face model
                    messages=[{"role": "user", "content": user_input}],
                )
                answer = response.choices[0].message.content
                st.write("**Assistant:**", answer)
            except Exception as e:
                st.error(f"❌ Error: {e}")
