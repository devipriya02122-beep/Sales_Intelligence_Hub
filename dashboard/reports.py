import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="devi",
        password="Mahipriya0212",
        database="sales_intelligence_db"
    )

def get_sales(branch_id=None):
    conn = get_connection()
    query = "SELECT * FROM customer_sales"
    if branch_id is not None:
        query += " WHERE branch_id = %s"
        df = pd.read_sql(query, conn, params=(branch_id,))
    else:
        df = pd.read_sql(query, conn)
    conn.close()
    return df

def reports_page():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please login first from the main page.")
        return

    st.title("📑 Reports")

    # --- Super Admin sees all branches ---
    if st.session_state["role"] == "Super Admin":
        df = get_sales()
        st.info("Showing reports for all branches")
    else:
        branch_id = st.session_state["branch_id"]
        df = get_sales(branch_id)
        st.info(f"Showing reports for branch ID {branch_id}")

    if df.empty:
        st.warning("No sales data available.")
        return

    # --- Branch comparison ---
    st.subheader("Branch Comparison")
    branch_summary = df.groupby("branch_id", as_index=False)[["gross_sales", "received_amount"]].sum()
    st.dataframe(branch_summary)

    fig = px.bar(branch_summary, x="branch_id", y="gross_sales",
                 title="Gross Sales by Branch", color="branch_id")
    st.plotly_chart(fig, use_container_width=True)

    # --- Product breakdown ---
    st.subheader("Product Breakdown")
    product_summary = df.groupby("product_name", as_index=False)["gross_sales"].sum()
    st.dataframe(product_summary)

    fig2 = px.pie(product_summary, names="product_name", values="gross_sales",
                  title="Sales Share by Product")
    st.plotly_chart(fig2, use_container_width=True)

    # --- Logout button ---
    if st.button("Logout", key="logout_reports"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["branch_id"] = None
        st.success("You have been logged out.")
        st.experimental_rerun()
