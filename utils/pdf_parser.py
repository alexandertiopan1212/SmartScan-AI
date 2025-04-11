import pdfplumber
import pandas as pd

def parse_pdf(file_path):
    full_text = ""
    tables = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text = page.extract_text()
            if text:
                full_text += text + "\n"

            # Extract tables
            page_tables = page.extract_tables()
            for table in page_tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])  # First row = header
                    tables.append(df)

    return full_text.strip(), tables