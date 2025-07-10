# app.py

import streamlit as st
import pandas as pd
from backend_metadata_fetcher import fetch_user_metadata_to_memory

st.set_page_config(page_title="📋 User Metadata Fetcher", layout="centered")
st.title("📋 Upload UID CSV to Fetch Metadata")

uploaded_file = st.file_uploader("Upload a CSV file with 'UID' column", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if 'UID' not in df.columns:
            st.error("The CSV must contain a column named 'UID'.")
        else:
            st.success("✅ File uploaded successfully. Processing metadata...")

            user_ids = df['UID'].unique().tolist()

            excel_stream, filename = fetch_user_metadata_to_memory(user_ids)

            st.download_button(
                label="📥 Download Excel",
                data=excel_stream,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error: {str(e)}")
