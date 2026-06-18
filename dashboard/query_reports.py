import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="devi",
        password="Mahipriya0212",
        database="sales_intelligence_db"
    )

# --- Categorized Queries ---
basic_queries = {
    "All Sales": "SELECT * FROM customer_sales",
    "All Branches": "SELECT * FROM branches",
    "All Payment Splits": "SELECT * FROM payment_splits",
    "Open Sales": "SELECT * FROM customer_sales WHERE status = 'Open'",
    "Branch Sales (Dynamic)": None  # handled with branch filter
}

aggregation_queries = {
    "Total Gross Sales": "SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales",
    "Total Received Amount": "SELECT SUM(received_amount) AS total_received FROM customer_sales",
    "Total Pending Amount": "SELECT SUM(pending_amount) AS total_pending FROM customer_sales",
    "Sales Count per Branch": "SELECT branch_id, COUNT(*) AS total_sales FROM customer_sales GROUP BY branch_id",
    "Average Gross Sales": "SELECT AVG(gross_sales) AS avg_gross_sales FROM customer_sales"
}

join_queries = {
    "Sales + Branch Name": "SELECT cs.sale_id, cs.name, cs.product_name, cs.gross_sales, b.branch_name FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id",
    "Sales + Total Payment": "SELECT cs.sale_id, cs.name, cs.gross_sales, SUM(ps.amount_paid) AS total_payment FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id GROUP BY cs.sale_id, cs.name, cs.gross_sales",
    "Branch-wise Gross Sales": "SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name",
    "Sales + Payment Method": "SELECT cs.sale_id, cs.name, cs.gross_sales, ps.payment_method, ps.amount_paid FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id",
    "Sales + Branch Admin": "SELECT cs.sale_id, cs.name, cs.gross_sales, b.branch_admin_name FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id"
}

financial_queries = {
    "Pending > 5000": "SELECT * FROM customer_sales WHERE pending_amount > 5000",
    "Top 3 Gross Sales": "SELECT sale_id, name, gross_sales FROM customer_sales ORDER BY gross_sales DESC LIMIT 3",
    "Branch with Highest Gross Sales": "SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name ORDER BY total_gross_sales DESC LIMIT 1",
    "Monthly Sales Summary (Dynamic)": None,  # handled with date filter
    "Payment Method-wise Collection": "SELECT payment_method, SUM(amount_paid) AS total_collection FROM payment_splits GROUP BY payment_method"
}

def run_query(query, selected_query):
    conn = get_connection()
    result_df = pd.read_sql(query, conn)
    conn.close()

    st.subheader(f"Report: {selected_query}")
    st.dataframe(result_df)

    # Auto charts for key reports
    if selected_query == "Branch-wise Gross Sales":
        fig = px.bar(result_df, x="branch_name", y="total_gross_sales",
                     title="Branch-wise Gross Sales", color="branch_name")
        st.plotly_chart(fig, use_container_width=True)

    elif selected_query == "Payment Method-wise Collection":
        fig = px.pie(result_df, names="payment_method", values="total_collection",
                     title="Payment Method-wise Collection")
        st.plotly_chart(fig, use_container_width=True)

    elif selected_query == "Monthly Sales Summary (Dynamic)":
        fig = px.line(result_df, x="month", y="monthly_sales", markers=True,
                      title="Monthly Sales Trend", color_discrete_sequence=["#FFD700"])
        st.plotly_chart(fig, use_container_width=True)

def reports_page():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please login first from the main page.")
        return

    st.title("📑 Reports")

    # --- Basic Queries ---
    st.subheader("🔹 Basic Queries")
    basic_choice = st.selectbox("Choose a basic report", list(basic_queries.keys()))
    if basic_choice == "Branch Sales (Dynamic)":
        conn = get_connection()
        branches_df = pd.read_sql("SELECT branch_name FROM branches", conn)
        conn.close()
        branch_choice = st.selectbox("Select Branch", branches_df["branch_name"].unique())
        if st.button("Run Branch Report"):
            query = f"""
                SELECT * 
                FROM customer_sales 
                WHERE branch_id IN (
                    SELECT branch_id FROM branches WHERE branch_name = '{branch_choice}'
                )
            """
            run_query(query, f"{branch_choice} Sales")
    else:
        if st.button("Run Basic Report"):
            run_query(basic_queries[basic_choice], basic_choice)

    # --- Aggregation Queries ---
    st.subheader("🔹 Aggregation Queries")
    agg_choice = st.selectbox("Choose an aggregation report", list(aggregation_queries.keys()))
    if st.button("Run Aggregation Report"):
        run_query(aggregation_queries[agg_choice], agg_choice)

    # --- Join-Based Queries ---
    st.subheader("🔹 Join-Based Queries")
    join_choice = st.selectbox("Choose a join-based report", list(join_queries.keys()))
    if st.button("Run Join Report"):
        run_query(join_queries[join_choice], join_choice)

    # --- Financial Tracking Queries ---
    st.subheader("🔹 Financial Tracking Queries")
    fin_choice = st.selectbox("Choose a financial report", list(financial_queries.keys()))
    if fin_choice == "Monthly Sales Summary (Dynamic)":
        start_date = st.date_input("Start Date", datetime.date(2024, 1, 1))
        end_date = st.date_input("End Date", datetime.date.today())
        if st.button("Run Monthly Report"):
            query = f"""
                SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(gross_sales) AS monthly_sales
                FROM customer_sales
                WHERE date BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY YEAR(date), MONTH(date)
                ORDER BY year, month
            """
            run_query(query, "Monthly Sales Summary (Dynamic)")
    else:
        if st.button("Run Financial Report"):
            run_query(financial_queries[fin_choice], fin_choice)

    # --- Logout button ---
    if st.button("Logout", key="logout_reports"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["branch_id"] = None
        st.success("You have been logged out.")
        st.experimental_rerun()
