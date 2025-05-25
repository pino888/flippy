import os
import streamlit as st
from scanner.file_scanner import find_excel_files
from scanner.metadata_extractor import extract_metadata
from ui.sidebar import show_sidebar
from ui.previewer import preview_file

st.set_page_config(layout="wide")
st.title("🐬 Flippy — Your Spreadsheets Navigator!", anchor=False)

folder, search = show_sidebar()

with st.spinner("Searching for files..."):
    if folder:
        all_files = find_excel_files(folder)

        # Step 1: Filter files BEFORE grouping
        matching_files = []

        for file in all_files:
            metadata = extract_metadata(file)

            # If there's a search term, filter it
            if search:
                search_lower = search.lower()
                found = search_lower in file.lower()

                for sheet in metadata["sheets"]:
                    if search_lower in sheet.lower():
                        found = True
                for cols in metadata["columns"].values():
                    if any(search_lower in col.lower() for col in cols):
                        found = True

                if not found:
                    continue  # Skip if not matching

            matching_files.append((file, metadata))  # Keep file + metadata

        # Step 2: Group filtered files by folder
        grouped_files = {}
        for file, metadata in matching_files:
            folder_name = os.path.dirname(file)
            grouped_files.setdefault(folder_name, []).append((file, metadata))

        if len(matching_files) == 0:
            st.error(f"🔍 No matching Excel files found")
        else:
            st.success(f"🔍 Found {len(matching_files)} matching Excel files across {len(grouped_files)} folders")

        # Step 3: Display grouped, filtered files
        for folder_name, files in grouped_files.items():
            with st.expander(f"📁 {folder_name} ({len(files)} files)", expanded=False):
                for idx, (file, metadata) in enumerate(files, start=1):
                    with st.container(border=True):
                        st.markdown(f"**File {idx} of {len(files)} — `{os.path.basename(file)}`**")
                        st.markdown("*Click sheet name below for details*")
                        preview_file(file, metadata)
    else:
        left_col, right_col = st.columns(2, border=True)
        left_col.markdown("""
            #### Tame Your Spreadsheet Chaos
            Flippy is a powerful yet lightweight app that helps you search, preview, 
            and explore Excel and CSV files right on your machine.  
              
            Whether you're drowning in spreadsheets or just trying to find that one column buried in a folder maze, 
            Flippy gives you instant answers — without opening a single file.  
            
            ---
            🔍 What You Can Do:  
            
            ✅ Scan folders, even network drives  
            ✅ Search filenames, sheets, or column headers  
            ✅ Preview Excel/CSV content without launching Excel  
            
            ---
            ✨ Why Use Flippy?  
            
            ✅ Secure & Private – Nothing gets uploaded  
            ✅ Saves hours of manual opening and scrolling  
            ✅ Helps you stay organized without changing tools  
            
            """)
        right_col.markdown("""
            #### How it works
            Follow these three simple steps, the rest is handled for you! 
            
            1️⃣ Enter folder path in the left panel and press Enter  
            2️⃣ Search for file names, sheets, or column headers  
            3️⃣ Instantly preview and explore results  
            
            """)
        # left_col_vid, mid_col_vid = st.columns(2, border=True)
        right_col.video("assets/demo.mov")

        st.markdown("""🔒 Your Data Stays Private""")
        st.markdown("*Flippy runs 100% locally — nothing is uploaded or shared online. "
                    "It only scans the folders you choose and never accesses anything else.*")
