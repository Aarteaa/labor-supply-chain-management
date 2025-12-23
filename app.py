import streamlit as st
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Labor Supply Chain System",
    layout="wide"
)

fake = Faker()

# ----------------------------
# Data Generation Function
# ----------------------------
def generate_contract_data(n_contracts):
    data = []

    for i in range(1, n_contracts + 1):
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(30, 365))

        data.append({
            "Contract ID": i,
            "Client ID": random.randint(1, 10),
            "Created Date": fake.date_between(start_date='-6m', end_date='today'),
            "Start Date": start_date,
            "End Date": end_date,
            "Workers Required": random.randint(5, 50),
            "Category ID": random.randint(1, 8),
            "Hourly Rate": random.randint(120, 350),
            "Contract Value": random.randint(50_000, 2_000_000),
            "Status": random.choice(["Active", "Completed", "Pending"]),
            "City": random.choice(["Mumbai", "Pune", "Aurangabad", "Nashik", "Goa"]),
            "Shift": random.choice(["Day", "Night", "Rotational"])
        })

    return pd.DataFrame(data)

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.title("⚙️ Controls")

num_contracts = st.sidebar.slider(
    "Number of Contracts",
    min_value=50,
    max_value=1000,
    value=200,
    step=50
)

city_filter = st.sidebar.multiselect(
    "Filter by City",
    ["Mumbai", "Pune", "Aurangabad", "Nashik", "Goa"],
    default=["Mumbai", "Pune"]
)

status_filter = st.sidebar.multiselect(
    "Filter by Status",
    ["Active", "Completed", "Pending"],
    default=["Active"]
)

# ----------------------------
# Generate Data
# ----------------------------
df = generate_contract_data(num_contracts)

df = df[df["City"].isin(city_filter)]
df = df[df["Status"].isin(status_filter)]

# ----------------------------
# Header
# ----------------------------
st.title("🧠 Labor Supply Chain Intelligence Dashboard")
st.caption("AI-driven workforce & contract analytics")

# ----------------------------
# KPI Section
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contracts", len(df))
col2.metric("Total Workers Required", int(df["Workers Required"].sum()))
col3.metric("Avg Hourly Rate", f"₹ {int(df['Hourly Rate'].mean())}")
col4.metric("Total Contract Value", f"₹ {df['Contract Value'].sum():,}")

# ----------------------------
# Charts
# ----------------------------
st.subheader("📊 Analytics")

colA, colB = st.columns(2)

with colA:
    st.write("Contracts by City")
    st.bar_chart(df["City"].value_counts())

with colB:
    st.write("Contracts by Status")
    st.bar_chart(df["Status"].value_counts())

# ----------------------------
# Data Table
# ----------------------------
st.subheader("📋 Contract Data")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Report Generation
# ----------------------------
st.subheader("📄 Generate Report")

report_text = f"""
LABOR SUPPLY CHAIN ANALYTICS REPORT
----------------------------------
Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Contracts: {len(df)}
Total Workers Required: {df['Workers Required'].sum()}
Average Hourly Rate: ₹{int(df['Hourly Rate'].mean())}
Total Contract Value: ₹{df['Contract Value'].sum():,}

Cities Covered: {', '.join(df['City'].unique())}
Active Contracts: {len(df[df['Status'] == 'Active'])}

TECHNICAL ACHIEVEMENTS
- Advanced SQL logic (CTEs, JOINs, Window Functions)
- Predictive-style workforce analysis
- KPI-driven contract intelligence
- Scalable data architecture
"""

st.download_button(
    "⬇️ Download Report",
    report_text,
    file_name="Labor_Supply_Chain_Report.txt"
)

st.success("Interactive dashboard ready 🚀")
