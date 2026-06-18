
# Sales Intelligence Hub 📊

A **Streamlit-powered analytics dashboard** for managing and visualizing sales data.  
This project integrates **dynamic SQL queries, branch filters, and financial tracking** to provide actionable insights for businesses.

---

## 🚀 Features
- **Authentication & Navigation** → Secure login with sidebar navigation.
- **Dashboard** → Quick overview of sales performance.
- **Sales Entry** → Add new sales records with payment splits.
- **Reports Page** → Organized into four categories:
  - 🔹 **Basic Queries** → View all sales, branches, payments, open sales, and branch-specific sales.
  - 🔹 **Aggregation Queries** → Totals, averages, and counts across sales and branches.
  - 🔹 **Join-Based Queries** → Sales with branch names, payments, admins, and grouped summaries.
  - 🔹 **Financial Tracking Queries** → Pending amounts, top sales, monthly summaries, and payment method collections.
- **Dynamic Filters**:
  - Branch filter → Select any branch instead of hardcoding.
  - Date range filter → Customize monthly sales summary.
- **Interactive Charts** → Auto-generated bar, pie, and line charts using Plotly.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Streamlit** (UI framework)
- **MySQL** (database)
- **Pandas** (data handling)
- **Plotly Express** (visualizations)

---

## 📂 Project Structure
```
Sales_Intelligence_Hub/
│
├── dashboard/
│   ├── app.py              # Main Streamlit app
│   ├── login.py            # Authentication page
│   ├── dashboard_page.py   # Dashboard view
│   ├── sales_entry_page.py # Sales entry form
│   └── query_reports.py    # Reports with categorized queries
│
├── reports.sql             # SQL queries reference
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/Sales_Intelligence_Hub.git
   cd Sales_Intelligence_Hub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run dashboard/app.py
   ```

---

## 📸 Screenshots
![
    ![alt text](image-1.png)
](image.png)
---![alt text](image-2.png)

## 📜 License
This project is licensed under the **MIT License** — free to use and modify.

---

## 👩‍💻 Author
**Devi Priya**  
Aspiring Data Analyst | Python & SQL Enthusiast | Streamlit Developer
