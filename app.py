#Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_excel("Superstore.xlsx")

# Set Streamlit app title
st.title("Minger Dashboard")

# Create a sidebar with tiles
with st.sidebar:
    selected_option = st.radio("Select an option:", ["Sales Overview", "Profit Analysis", "Product Insights"])

# Filter options
if selected_option == "Sales Overview":
    st.sidebar.subheader("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", min(df["Order Date"]))
    end_date = st.sidebar.date_input("End Date", max(df["Order Date"]))

    # Convert start_date and end_date to datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    st.subheader("Monthly Sales Trend")
    filtered_sales = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
    st.line_chart(filtered_sales.set_index("Order Date")["Sales"])

    st.subheader("Sales by Product Category")
    category_sales = filtered_sales.groupby("Category")["Sales"].sum()
    st.bar_chart(category_sales)

elif selected_option == "Profit Analysis":
    st.sidebar.subheader("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", min(df["Order Date"]))
    end_date = st.sidebar.date_input("End Date", max(df["Order Date"]))

    # Convert start_date and end_date to datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    st.subheader("Profit Trend over Time")
    filtered_profit = df[(df["Order Date"] >= start_date) & (df["Order Date"] <= end_date)]
    st.line_chart(filtered_profit.set_index("Order Date")["Profit"])

    st.subheader("Profit vs. Discount")
    sns.scatterplot(data=filtered_profit, x="Discount", y="Profit")
    st.pyplot(plt)

elif selected_option == "Product Insights":
    selected_product = st.selectbox("Select a product:", df["Product Name"].unique())
    product_df = df[df["Product Name"] == selected_product]

    st.subheader(f"Sales and Profit for {selected_product}")
    st.bar_chart(product_df[["Sales", "Profit"]])
