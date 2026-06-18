import streamlit as st
import mysql.connector
import bcrypt

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="devi",
        password="Mahipriya0212",
        database="sales_intelligence_db"
    )

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            st.session_state["authenticated"] = True
            st.session_state["role"] = user["role"]
            st.session_state["branch_id"] = user["branch_id"]
            st.success("Login successful! Redirecting to Dashboard...")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
