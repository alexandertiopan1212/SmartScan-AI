import streamlit as st
import os
from datetime import datetime
from io import StringIO
import logging
import warnings
import pandas as pd

from utils.pdf_parser import parse_pdf
from utils.image_ocr import extract_text_from_image
from utils.matcher import compare_invoice_po
from utils.export import export_results
from utils.chatbot_llm import ask_openrouter

# --- Environment config ---
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
warnings.filterwarnings("ignore")
logging.getLogger("torch").setLevel(logging.ERROR)

# --- Streamlit config ---
st.set_page_config(page_title="SmartScan AI", layout="wide")
st.title("🧠 SmartScan AI: Finance Doc Analyzer")
st.caption("Upload your scanned Invoice & PO (PDF or Image), and let AI do the matching!")

# --- Sidebar Upload ---
st.sidebar.header("📤 Upload Files")
invoice_file = st.sidebar.file_uploader("Upload Invoice", type=["pdf", "png", "jpg", "jpeg"], key="invoice_file")
po_file = st.sidebar.file_uploader("Upload Purchase Order (PO)", type=["pdf", "png", "jpg", "jpeg"], key="po_file")
export_btn = st.sidebar.button("📁 Export Result")

# --- Ensure directories ---
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/results", exist_ok=True)

# --- Session state ---
for key in ["invoice_text", "invoice_tables", "last_invoice_name",
            "po_text", "po_tables", "last_po_name",
            "match_result", "last_export_path"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- Table Fallback ---
def clean_and_parse_table(text):
    lines = text.strip().splitlines()
    lines = [line for line in lines if "," in line]
    csv_data = "\n".join(lines)
    return pd.read_csv(StringIO(csv_data))

# --- Main content ---
if invoice_file and po_file:
    invoice_path = f"data/uploads/invoice_{invoice_file.name}"
    po_path = f"data/uploads/po_{po_file.name}"
    with open(invoice_path, "wb") as f: f.write(invoice_file.getbuffer())
    with open(po_path, "wb") as f: f.write(po_file.getbuffer())
    st.success("✅ Both files uploaded!")

    # Reset session
    if invoice_file.name != st.session_state.last_invoice_name:
        st.session_state.invoice_text = ""
        st.session_state.invoice_tables = None
        st.session_state.match_result = None
        st.session_state.last_invoice_name = invoice_file.name
    if po_file.name != st.session_state.last_po_name:
        st.session_state.po_text = ""
        st.session_state.po_tables = None
        st.session_state.match_result = None
        st.session_state.last_po_name = po_file.name

    # --- Invoice ---
    st.subheader("📄 Extracted Invoice")
    if not st.session_state.invoice_text:
        if invoice_path.endswith(".pdf"):
            text, tables = parse_pdf(invoice_path)
        else:
            text = extract_text_from_image(invoice_path)
            tables = None
        if not tables:
            try: tables = [clean_and_parse_table(text)]
            except: tables = None
        st.session_state.invoice_text = text
        st.session_state.invoice_tables = tables

    st.text_area("🧾 Invoice Text", st.session_state.invoice_text, height=200)
    if st.session_state.invoice_tables:
        st.write("📊 Invoice Table Preview")
        st.dataframe(st.session_state.invoice_tables[0])

    # --- PO ---
    st.subheader("📄 Extracted Purchase Order")
    if not st.session_state.po_text:
        if po_path.endswith(".pdf"):
            text, tables = parse_pdf(po_path)
        else:
            text = extract_text_from_image(po_path)
            tables = None
        if not tables:
            try: tables = [clean_and_parse_table(text)]
            except: tables = None
        st.session_state.po_text = text
        st.session_state.po_tables = tables

    st.text_area("📋 PO Text", st.session_state.po_text, height=200)
    if st.session_state.po_tables:
        st.write("📊 PO Table Preview")
        st.dataframe(st.session_state.po_tables[0])

    # --- Matching ---
    st.subheader("🔍 Invoice vs PO Matching Result")
    if st.session_state.invoice_tables and st.session_state.po_tables and not st.session_state.match_result:
        try:
            st.session_state.match_result = compare_invoice_po(
                st.session_state.invoice_tables[0],
                st.session_state.po_tables[0]
            )
        except Exception as e:
            st.session_state.match_result = {"status": "Error", "details": [str(e)]}

    if st.session_state.match_result:
        st.markdown(f"**Status:** `{st.session_state.match_result['status']}`")
        if st.session_state.match_result["details"]:
            st.write("📌 **Details:**")
            for detail in st.session_state.match_result["details"]:
                st.markdown(f"- {detail}")
        else:
            st.success("🎉 No discrepancies found. Invoice and PO match perfectly!")

    # --- Export ---
    if export_btn:
        result_paths = export_results(
            st.session_state.invoice_tables[0],
            st.session_state.po_tables[0],
            st.session_state.match_result,
        )
        st.session_state.last_export_path = result_paths
        st.success("✅ Exported result files to `data/results`")

    if st.session_state.last_export_path:
        st.subheader("📤 Download Exported Files")
        with open(st.session_state.last_export_path["invoice_csv"], "rb") as f:
            st.download_button("⬇️ Download Invoice CSV", data=f.read(), file_name=os.path.basename(st.session_state.last_export_path["invoice_csv"]), mime="text/csv")
        with open(st.session_state.last_export_path["po_csv"], "rb") as f:
            st.download_button("⬇️ Download PO CSV", data=f.read(), file_name=os.path.basename(st.session_state.last_export_path["po_csv"]), mime="text/csv")
        with open(st.session_state.last_export_path["report_pdf"], "rb") as f:
            st.download_button("⬇️ Download PDF Report", data=f.read(), file_name=os.path.basename(st.session_state.last_export_path["report_pdf"]), mime="application/pdf")

# --- Chatbot Sidebar ---
with st.sidebar.expander("🧠 Ask AI about the documents"):
    st.markdown("Ask anything about your uploaded invoice or PO:")
    user_prompt = st.text_area("💬 Your question")
    if st.button("Ask AI"):
        if user_prompt.strip():
            with st.spinner("Thinking..."):
                ai_reply = ask_openrouter(user_prompt)
            st.markdown("**AI says:**")
            st.success(ai_reply)
        else:
            st.warning("Please type a question first.")
