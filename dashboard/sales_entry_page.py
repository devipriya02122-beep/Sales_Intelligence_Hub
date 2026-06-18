import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="devi",
        password="Mahipriya0212",
        database="sales_intelligence_db"
    )

def sales_entry_page():
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("Please login first from the main page.")
        return

    st.title("➕ Sales Entry & Payments")

    # Add new sales entry
    with st.form("add_sale_form"):
        customer_name = st.text_input("Customer Name")
        mobile_number = st.text_input("Mobile Number")
        product_name = st.selectbox("Product", ["DS","DA","BA","FSD","ML","SQL"])
        gross_sales = st.number_input("Gross Sales", min_value=0.0, format="%.2f")

        if st.session_state["role"] == "Super Admin":
            branch_id = st.number_input("Branch ID", min_value=1)
        else:
            branch_id = st.session_state["branch_id"]

        submitted = st.form_submit_button("Insert Sale")
        if submitted:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status) VALUES (%s, CURDATE(), %s, %s, %s, %s, 'Open')",
                (branch_id, customer_name, mobile_number, product_name, gross_sales)
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Sale added successfully!")

    # Add payment split
    with st.form("add_payment_form"):
        sale_id = st.number_input("Sale ID", min_value=1)
        amount_paid = st.number_input("Amount Paid", min_value=0.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", ["Cash","UPI","Card"])
        submitted = st.form_submit_button("Insert Payment")
        if submitted:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES (%s, CURDATE(), %s, %s)",
                (sale_id, amount_paid, payment_method)
            )
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Payment split added successfully!")

    # --- Logout button ---
    if st.button("Logout", key="logout_sales_entry"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["branch_id"] = None
        st.success("You have been logged out.")
        st.experimental_rerun()
