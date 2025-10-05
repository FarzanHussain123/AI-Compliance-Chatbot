import os
import requests
import streamlit as st

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # ✅ new working public model

st.set_page_config(page_title="OSS Compliance Chatbot 💬", page_icon="💬")
st.title("OSS Compliance Chatbot 💬")
st.write("Ask me about OSS compliance:")

user_input = st.text_input("Your question:")

def hf_generate(prompt):
    if not HF_TOKEN:
        return "⚠️ Hugging Face API token missing. Add HF_TOKEN in Streamlit → App Settings → Secrets."
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300}, "options": {"wait_for_model": True}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        output = r.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        return str(output)
    except Exception as e:
        return f"❌ Error calling Hugging Face API: {e}"

if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            answer = hf_generate(user_input)
        st.write("**Assistant:**", answer)
