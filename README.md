# 🧠 SmartScan AI

SmartScan AI is a powerful web app built with Streamlit that lets you upload scanned **Invoice** and **Purchase Order (PO)** documents (PDF or image), extract their content using OCR and PDF parsing, and automatically **compare** the data to detect discrepancies. It also includes an **AI chatbot** powered by OpenRouter to help users understand the content of uploaded documents.

---

## 🚀 Features

- 📤 Upload Invoice & PO in **PDF, JPG, PNG, JPEG**
- 📄 Extract text and tables from documents using OCR/PDF parser
- 🔍 **Auto-match** invoice vs PO line items (qty, price, total)
- 📁 Export results to **CSV + PDF comparison report**
- 🤖 Built-in **AI Chatbot** for document-related Q&A (powered by OpenRouter)
- ✅ Streamlit-compatible for easy local or cloud deployment

---

## 📦 Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/smartscan-ai.git
cd smartscan-ai
```

2. Install dependencies (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

3. Create a `secrets.toml` file in `.streamlit/` folder:

```toml
# .streamlit/secrets.toml
[openrouter]
api_key = "your_openrouter_api_key_here"
```

> Get a free API key from [https://openrouter.ai](https://openrouter.ai)

---

## 🧪 Usage

Run locally with:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`.

---

## 📤 Deployment (Streamlit Cloud)

1. Push your repo to GitHub
2. Create a new app on [https://share.streamlit.io](https://share.streamlit.io)
3. Add your OpenRouter API key under **Secrets** as:

```
[openrouter]
api_key = "your-api-key"
```

That's it — your app is live!

---

## 📚 Example Use Case

1. Upload scanned Invoice and PO files
2. View extracted tables and text
3. See side-by-side **discrepancy check** (e.g. quantity or price mismatch)
4. Ask AI: "Why are my invoice and PO different?"
5. Download the report for your finance team.

---

## 🛠️ Tech Stack

- 🐍 Python
- 🎈 Streamlit
- 📄 PyMuPDF, pdfplumber, pytesseract
- 🔎 pandas, re
- 🤖 OpenRouter API (LLM)

---

## 📃 License

MIT License