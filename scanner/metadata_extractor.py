import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def extract_metadata(file_path, max_rows=5):
    metadata = {"sheets": [], "columns": {}}
    try:
        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path, nrows=max_rows)
            metadata["sheets"] = ["CSV"]
            metadata["columns"]["CSV"] = list(df.columns)

        else:
            xl = pd.ExcelFile(file_path, engine="openpyxl")
            metadata["sheets"] = xl.sheet_names

            for sheet in xl.sheet_names:
                try:
                    df = xl.parse(sheet, nrows=max_rows)
                    metadata["columns"][sheet] = list(df.columns)
                except Exception as e:
                    metadata["columns"][sheet] = [f"<Sheet error: {e}>"]

    except Exception as e:
        metadata["sheets"] = [f"<Error: {e}>"]
        metadata["columns"] = {}

    return metadata
