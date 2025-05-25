import streamlit as st
import pandas as pd


def preview_file(file_path, metadata):
    """
    Displays file preview - sheets names if applicable, column headers, and top 5 rows of the file
    :param file_path: full path to the file
    :param metadata: metadata from the scanned directory
    :return DataFrame:
    """
    tabs = st.tabs(["📑"+_ for _ in metadata["sheets"][:10]])
    c = 0

    for sheet in metadata["sheets"][:10]:
        with tabs[c]:
            cols = metadata["columns"].get(sheet, [])
            st.markdown(f"**Total Columns ({len(cols)}):** "+", ".join(cols))
            c += 1

        # with tab2:
            try:
                if st.button(f"Click to Preview", key=f"btn-{file_path}-{sheet}", type="primary"):
                    with st.spinner("Loading preview..."):
                        if file_path.lower().endswith(".csv"):
                            df = pd.read_csv(file_path, nrows=5)
                        else:
                            df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)

                        st.dataframe(df)

            except Exception as e:
                st.warning(f"⚠️ Could not preview file: {e}")
