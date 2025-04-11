# utils/chatbot_llm.py

import requests
import streamlit as st

def ask_openrouter(prompt, model="mistralai/mistral-7b-instruct"):
    api_key = st.secrets["openrouter"]["api_key"]

    # Context injection
    invoice_text = st.session_state.get("invoice_text", "")[:1000]
    po_text = st.session_state.get("po_text", "")[:1000]

    system_prompt = f"""
You are a helpful assistant. Analyze the following uploaded documents:

INVOICE:
{invoice_text}

PURCHASE ORDER:
{po_text}

Then answer the user question in a concise and helpful way.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://smartscan.streamlit.app",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"
