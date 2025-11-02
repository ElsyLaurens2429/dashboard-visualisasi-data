# Sample Streamlit app for the dashboard mockup (needs streamlit and plotly)
import streamlit as st
import pandas as pd
import plotly.express as px

# Load sample data (CSV expected in same folder)
df = pd.read_csv("sample_sales_2022.csv", parse_dates=["date"])

st.set_page_config(layout="wide", page_title="Business Performance Dashboard")

# Top KPI metrics
total_sales = df["before_discount"].sum()
net_profit = int(total_sales * 0.22)
aov = total_sales / df["quantity"].sum()
unique_customers = df["unique_customers"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Net Profit", f"{net_profit:,.0f}")
col3.metric("AOV", f"{aov:.2f}")
col4.metric("Unique Customers", f"{unique_customers:,.0f}")

# Filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2022-12-31"))
category = st.sidebar.multiselect("Category", options=df["category"].unique(), default=df["category"].unique())

filtered = df[(df["date"]>=pd.to_datetime(start_date)) & (df["date"]<=pd.to_datetime(end_date)) & (df["category"].isin(category))]

# Monthly trend
monthly = filtered.groupby(filtered["date"].dt.to_period("M"))["before_discount"].sum().reset_index()
monthly["date"] = monthly["date"].dt.to_timestamp()
fig = px.line(monthly, x="date", y="before_discount", title="Monthly Sales")
st.plotly_chart(fig, use_container_width=True)

# Category revenue
cat_rev = filtered.groupby("category")["before_discount"].sum().reset_index().sort_values(by="before_discount", ascending=False)
fig2 = px.bar(cat_rev, x="category", y="before_discount", title="Revenue by Category")
st.plotly_chart(fig2, use_container_width=True)
