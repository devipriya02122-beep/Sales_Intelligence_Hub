import pandas as pd
import mysql.connector
import bcrypt

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="devi",          # your MySQL user
    password="Mahipriya0212",
    database="sales_intelligence_db"
)
cursor = conn.cursor()

def load_users(csv_file):
    df = pd.read_csv(csv_file)

    # Drop auto-increment column if present
    if 'user_id' in df.columns:
        df = df.drop(columns=['user_id'])

    # Replace NaN with None
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        # Ensure branch_id is None if blank/NaN
        if row["branch_id"] is None or str(row["branch_id"]).lower() == "nan":
            row["branch_id"] = None

        # Hash password before insertion
        raw_pw = row["password"]
        if raw_pw is not None:
            hashed_pw = bcrypt.hashpw(raw_pw.encode("utf-8"), bcrypt.gensalt())
            row["password"] = hashed_pw.decode("utf-8")

        sql = """
        INSERT INTO users (username, password, branch_id, role, email)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                row["username"],
                row["password"],
                row["branch_id"],
                row["role"],
                row["email"]
            ))
            print("Inserted:", row["username"], row["email"])
        except Exception as e:
            print("Error inserting row:", e)

    conn.commit()
    print(f"Inserted {len(df)} rows into users")

# Use your actual path
load_users(r"C:\Users\Priya\OneDrive\Priya\Project\Sales_Intelligence_Hub\datasets\users.csv")

cursor.close()
conn.close()
