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

def dashboard_page():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please login first from the main page.")
        return

    st.title("📊 Sales Intelligence Hub - Dashboard")

    # --- Super Admin logic ---
    if st.session_state["role"] == "Super Admin":
        df = get_sales()
        st.info("Showing data for all branches")

        # Ensure branch_id values are integers
        branch_options = sorted([int(b) for b in df["branch_id"].unique().tolist()])
        selected_branch = st.selectbox("Filter by Branch", ["All"] + branch_options)

        if selected_branch != "All":
            # No int() conversion needed, already integer
            df = df[df["branch_id"] == selected_branch]

    # --- Admin logic ---
    else:
        branch_id = st.session_state["branch_id"]
        df = get_sales(branch_id)
        st.info(f"Showing data for branch ID {branch_id}")

    # --- Debug line (optional) ---
    st.write("Rows loaded:", len(df))

    # --- KPIs ---
    total_sales = df['gross_sales'].sum()
    received_amount = df['received_amount'].sum()
    pending_amount = total_sales - received_amount
    pending_percentage = (pending_amount / total_sales * 100) if total_sales > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    col2.metric("✅ Received Amount", f"{received_amount:,.0f}")
    col3.metric("⚠️ Pending Amount", f"{pending_amount:,.0f}")
    col4.metric("📉 Pending %", f"{pending_percentage:.2f}%")

    # --- Charts ---
    col5, col6 = st.columns(2)
    with col5:
        fig1 = px.bar(df.groupby("product_name", as_index=False)["gross_sales"].sum(),
                      x="product_name", y="gross_sales", color="product_name",
                      title="Sales by Product")
        st.plotly_chart(fig1, use_container_width=True)
    with col6:
        fig2 = px.pie(df, names="status", values="gross_sales",
                      title="Sales Status Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Daily Sales Trend")
    df["date"] = pd.to_datetime(df["date"])
    trend = df.groupby("date", as_index=False)["gross_sales"].sum()
    fig3 = px.line(trend, x="date", y="gross_sales", markers=True,
                   color_discrete_sequence=["#FFD700"])
    st.plotly_chart(fig3, use_container_width=True)

    # --- Logout button ---
    if st.button("Logout", key="logout_dashboard"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["branch_id"] = None
        st.success("You have been logged out.")
        st.experimental_rerun()
