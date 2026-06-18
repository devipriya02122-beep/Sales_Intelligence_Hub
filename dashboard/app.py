import streamlit as st
from login import login_page
from dashboard_page import dashboard_page
from sales_entry_page import sales_entry_page
from query_reports import reports_page

def main():
    # --- Authentication check ---
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_page()
        return

    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Dashboard", "Sales Entry", "Reports"])

    if choice == "Dashboard":
        dashboard_page()
    elif choice == "Sales Entry":
        sales_entry_page()
    elif choice == "Reports":
        reports_page()

if __name__ == "__main__":
    main()
