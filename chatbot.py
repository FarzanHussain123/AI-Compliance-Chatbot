import os
from openai import OpenAI
import streamlit as st

# ====== Hugging Face Inference Configuration ======
HF_TOKEN = os.getenv("HF_TOKEN")  # from Streamlit Secrets

# Initialize OpenAI client but point to Hugging Face router
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# ====== Streamlit UI ======
st.set_page_config(page_title="OSS Compliance Chatbot 💬", page_icon="💬")
st.title("OSS Compliance Chatbot 💬")
st.write("Ask me about OSS compliance:")

user_input = st.text_input("Your question:")

# ====== Model Fallback List ======
# These are all chat-style models hosted on Hugging Face’s OpenAI-compatible API.
MODEL_LIST = [
    "meta-llama/Meta-Llama-3-8B-Instruct",   # ChatGPT-like
    "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Strong, may be slower
    "HuggingFaceH4/zephyr-7b-beta:featherless-ai",  # Backup
    "google/flan-t5-base"                    # Last fallback (small but always accessible)
]


def query_model(prompt: str):
    """Try models one by one until one responds successfully."""
    for model_name in MODEL_LIST:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.choices[0].message.content
            return f"**Model:** {model_name}\n\n{answer}"
        except Exception as e:
            st.info(f"⚠️ {model_name} unavailable: {e}")
    return "❌ All models failed. Try again later or check your Hugging Face token."


# ====== Chat Logic ======
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = query_model(user_input)
        st.write("**Assistant:**", result)
