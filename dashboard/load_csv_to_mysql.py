import pandas as pd
import mysql.connector
import bcrypt

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="devi",
    password="Mahipriya0212",
    database="sales_intelligence_db"
)
cursor = conn.cursor()

def load_csv_to_table(cursor, conn, csv_file, table_name, columns, drop_cols=None, hash_password=False):
    df = pd.read_csv(csv_file)

    # Drop unwanted columns
    if drop_cols:
        for col in drop_cols:
            if col in df.columns:
                df = df.drop(columns=[col])

    # Replace NaN with None
    df = df.where(pd.notnull(df), None)

    for _, row in df.iterrows():
        values = []
        for col in columns:
            val = row[col]

            # Explicitly fix NaN/None
            if val is None or str(val).lower() == "nan":
                val = None

            # Hash password if needed
            if hash_password and col == "password" and val is not None:
                val = bcrypt.hashpw(val.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            values.append(val)

        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        try:
            cursor.execute(sql, tuple(values))
            print(f"Inserted row into {table_name}: {values}")
        except Exception as e:
            print(f"Error inserting row into {table_name}: {e}")

    conn.commit()
    print(f"Inserted {len(df)} rows into {table_name}")

# --- Load tables ---
load_csv_to_table(cursor, conn,
    r"C:\Users\Priya\OneDrive\Priya\Project\Sales_Intelligence_Hub\datasets\branches.csv",
    "branches", ["branch_name", "branch_admin_name"], drop_cols=["branch_id"])

load_csv_to_table(cursor, conn,
    r"C:\Users\Priya\OneDrive\Priya\Project\Sales_Intelligence_Hub\datasets\users.csv",
    "users", ["username", "password", "branch_id", "role", "email"],
    drop_cols=["user_id"], hash_password=True)

load_csv_to_table(cursor, conn,
    r"C:\Users\Priya\OneDrive\Priya\Project\Sales_Intelligence_Hub\datasets\customer_sales.csv",
    "customer_sales", ["branch_id", "date", "name", "mobile_number", "product_name", "gross_sales", "received_amount", "status"],
    drop_cols=["sale_id"])

load_csv_to_table(cursor, conn,
    r"C:\Users\Priya\OneDrive\Priya\Project\Sales_Intelligence_Hub\datasets\payment_splits.csv",
    "payment_splits", ["sale_id", "payment_date", "amount_paid", "payment_method"],
    drop_cols=["payment_id"])

cursor.close()
conn.close()
