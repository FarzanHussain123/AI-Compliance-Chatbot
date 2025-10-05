import os
import requests
import streamlit as st

# ====== Configuration ======
HF_TOKEN = os.getenv("HF_TOKEN")  # from Streamlit Secrets
HF_MODEL = "google/flan-t5-large"  # ✅ your selected model

# ====== Streamlit UI ======
st.set_page_config(page_title="OSS Compliance Chatbot 💬", page_icon="💬")
st.title("OSS Compliance Chatbot 💬")
st.write("Ask me about OSS compliance:")

user_input = st.text_input("Your question:")

# ====== Helper: Hugging Face Inference ======
def hf_generate(prompt):
    if not HF_TOKEN:
        return "⚠️ Hugging Face API token missing. Please add HF_TOKEN in Streamlit → App Settings → Secrets."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        output = response.json()
        # The response is usually a list with generated_text
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        # For some models, the output is a dictionary
        if isinstance(output, dict) and "generated_text" in output:
            return output["generated_text"]
        return str(output)
    except Exception as e:
        return f"❌ Error calling Hugging Face API: {e}"

# ====== Run Chatbot ======
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            answer = hf_generate(user_input)
        st.write("**Assistant:**", answer)
