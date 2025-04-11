import pandas as pd

def normalize_columns(df):
    """
    Standardize column names: lowercase, strip spaces, replace "/" with underscore.
    """
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )
    return df

def try_split_single_column(df):
    """
    If the DataFrame has only one column, try to split it into multiple columns using commas.
    """
    if df.shape[1] == 1:
        try:
            # Split by comma
            new_df = df.iloc[:, 0].astype(str).str.split(",", expand=True)
            # Use first row as header
            new_df.columns = new_df.iloc[0]
            return new_df[1:].reset_index(drop=True)
        except Exception:
            return df
    return df

def compare_invoice_po(invoice_data, po_data):
    """
    Compare invoice and PO DataFrames for matching key columns.
    """
    result = {
        "status": "Match",
        "details": []
    }

    try:
        invoice_df = try_split_single_column(invoice_data.copy())
        po_df = try_split_single_column(po_data.copy())

        if invoice_df.shape[1] == 1 or po_df.shape[1] == 1:
            result["status"] = "Error"
            result["details"].append("❌ Detected only 1 column. Please upload structured PDF with clearly defined tables.")
            return result

        invoice_df = normalize_columns(invoice_df)
        po_df = normalize_columns(po_df)

        # Define the common structure you're expecting
        key_columns = ["item", "qty", "price_unit", "total"]

        for col in key_columns:
            if col in invoice_df.columns and col in po_df.columns:
                inv_col = invoice_df[col].astype(str).str.lower().str.strip()
                po_col = po_df[col].astype(str).str.lower().str.strip()
                if not inv_col.equals(po_col):
                    result["status"] = "Mismatch"
                    result["details"].append(f"⚠️ Column '{col}' has discrepancies.")
            else:
                result["status"] = "Mismatch"
                result["details"].append(f"⚠️ Column '{col}' missing in one of the documents.")

    except Exception as e:
        result["status"] = "Error"
        result["details"].append(f"❌ Unexpected error: {str(e)}")

    return result
