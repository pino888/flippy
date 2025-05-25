import streamlit as st


def clear_search():
    st.session_state["search"] = ""


def clear_folder():
    st.session_state["folder"] = ""
    st.session_state["search"] = ""
    st.session_state["trigger_rerun"] = True  # Set rerun flag


def show_sidebar():
    # st.sidebar.markdown("## 📁 Folder & Search")

    # Text inputs
    folder = st.sidebar.text_input(
        "📁 Enter folder path",
        value=st.session_state.get("folder", ""),
        placeholder="C:\\Users\\yourname\\Documents",
        key="folder"
    )

    search = None
    if folder:
        search = st.sidebar.text_input(
            "🔍 Search within the files",
            value=st.session_state.get("search", ""),
            placeholder="file or column name e.g. 'date'",
            key="search"
        )

        # Clear buttons
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.button("🧹 Clear Path", on_click=clear_folder)
        with col2:
            st.button("❌ Clear Filter", on_click=clear_search)

    # Manually trigger rerun if flag is set
    if st.session_state.get("trigger_rerun", False):
        st.session_state["trigger_rerun"] = False  # Reset flag
        st.rerun()

    return folder.strip(), search.strip() if search else None


# def show_sidebar():
#    folder = st.sidebar.text_input("📁 Enter folder path", "", placeholder="C:\\Users")
#    if folder:
#        search = st.sidebar.text_input("🔍 Search within the files", "", placeholder="file or a column name e.g 'date'")
#        return folder.strip(), search.strip()
#    return folder.strip(), None
