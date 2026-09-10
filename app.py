import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("sales_data.csv")

    # Convert Order_Date into datetime
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    # Create Month column
    df["Month"] = df["Order_Date"].dt.strftime("%b")

    return df


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("📊 Sales Analytics Dashboard")

st.write(
    "Interactive dashboard for analyzing sales, profit, "
    "customers, products and regional performance."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")


# Category Filter
category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)


# Region Filter
region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)


# Product Filter
product = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Product"].isin(product))
]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_customers = filtered_df["Customer"].nunique()

total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "💰 Total Sales",
    f"₹{total_sales:,.0f}"
)


col2.metric(
    "📈 Total Profit",
    f"₹{total_profit:,.0f}"
)


col3.metric(
    "📦 Total Orders",
    total_orders
)


col4.metric(
    "👥 Customers",
    total_customers
)


col5, col6 = st.columns(2)


col5.metric(
    "🛒 Quantity Sold",
    total_quantity
)


col6.metric(
    "💵 Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# =========================================================
# SEPARATOR
# =========================================================

st.divider()


# =========================================================
# SALES BY CATEGORY
# =========================================================

st.subheader("📊 Sales by Category")


category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)


fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Total Sales by Category",
    text_auto=True
)


fig_category.update_layout(
    xaxis_title="Category",
    yaxis_title="Sales"
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)


# =========================================================
# SALES BY REGION
# =========================================================

st.subheader("🌍 Sales by Region")


region_sales = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)


fig_region = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Sales Distribution by Region",
    hole=0.4
)


st.plotly_chart(
    fig_region,
    use_container_width=True
)


# =========================================================
# MONTHLY SALES TREND
# =========================================================

st.subheader("📈 Monthly Sales Trend")


monthly_sales = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .reindex(
        ["Jan", "Feb", "Mar", "Apr",
         "May", "Jun", "Jul", "Aug",
         "Sep", "Oct", "Nov", "Dec"]
    )
    .dropna()
    .reset_index()
)


fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)


fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales"
)


st.plotly_chart(
    fig_month,
    use_container_width=True
)


# =========================================================
# PROFIT BY CATEGORY
# =========================================================

st.subheader("💰 Profit by Category")


category_profit = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .reset_index()
)


fig_profit = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    title="Profit by Category",
    text_auto=True
)


st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# =========================================================
# TOP PRODUCTS
# =========================================================

st.subheader("🏆 Top Products")


top_products = (
    filtered_df
    .groupby("Product")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values(
        by="Sales",
        ascending=False
    )
    .reset_index()
)


fig_products = px.bar(
    top_products,
    x="Product",
    y="Sales",
    title="Top Products by Sales",
    text_auto=True
)


st.plotly_chart(
    fig_products,
    use_container_width=True
)


# =========================================================
# DATA TABLE
# =========================================================

st.subheader("📋 Sales Data")


st.dataframe(
    filtered_df,
    use_container_width=True
)


# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

csv_data = filtered_df.to_csv(index=False)


st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Sales Analytics Dashboard | Built with Python, Pandas, "
    "Streamlit and Plotly"
)