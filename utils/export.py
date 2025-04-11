import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

def export_results(invoice_df, po_df, comparison_result, output_dir="data/results"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    invoice_csv_path = os.path.join(output_dir, f"invoice_{timestamp}.csv")
    po_csv_path = os.path.join(output_dir, f"po_{timestamp}.csv")
    report_pdf_path = os.path.join(output_dir, f"comparison_report_{timestamp}.pdf")

    invoice_df.to_csv(invoice_csv_path, index=False)
    po_df.to_csv(po_csv_path, index=False)

    # Create PDF report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Invoice vs PO Comparison Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Comparison Status: {comparison_result['status']}", ln=True)
    
    if comparison_result["details"]:
        pdf.ln(5)
        pdf.cell(200, 10, txt="Details:", ln=True)
        for detail in comparison_result["details"]:
            pdf.multi_cell(0, 8, txt=f"- {detail}".encode('latin-1', 'replace').decode('latin-1'))

    pdf.output(report_pdf_path)

    return {
        "invoice_csv": invoice_csv_path,
        "po_csv": po_csv_path,
        "report_pdf": report_pdf_path
    }
