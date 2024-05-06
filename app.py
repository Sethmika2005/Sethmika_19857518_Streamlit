#Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
df = pd.read_excel("Superstore.xlsx")

# Set Streamlit app title
st.title("Minger Dashboard")

# Create a sidebar with tiles
with st.sidebar:
    selected_option = st.radio("Select an option:", ["Sales Overview", "Profit Analysis", "Product Insights"])

#Colour palete
colour_palete=['#357b72', '#6b9b8e', '#99bcb5', '#c8dedb']

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

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales by Segment")
        segment_sales = px.pie(filtered_sales.groupby("Segment")["Sales"].sum(), values='Sales', names=filtered_sales.groupby("Segment")["Sales"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(segment_sales, use_container_width=True)
        
    with col2:
        st.subheader("Sales by Category")
        category_sales = px.pie(filtered_sales.groupby("Category")["Sales"].sum(), values='Sales', names=filtered_sales.groupby("Category")["Sales"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(category_sales, use_container_width=True)
   
    # Sum of Sales by Market
    st.subheader("Sales by Market")
    market_sales = filtered_sales.groupby("Market")["Sales"].sum()
    st.bar_chart(market_sales, color='#357b72')

    # Create the scatter plot with customized background color
    plt.figure(figsize=(8,6), facecolor='#E8E8E8')
    sns.set_style("white")  # Remove grid lines
    plt.rcParams['axes.facecolor'] = '#E8E8E8'  # Set background color
    sns.scatterplot(data=filtered_sales, x="Discount", y="Profit", color='#357b72')
    # Display the plot
    st.pyplot(plt)

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

    # Sum of Sales by Segment and by Category
    # Create columns for layout
    col1, col2 = st.columns(2)
    with col1:   
        # Sum of Profit by Segment
        st.subheader("Profit by Segment")
        segment_profit = px.pie(filtered_profit.groupby("Segment")["Profit"].sum(), values='Profit', names=filtered_profit.groupby("Segment")["Profit"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(segment_profit, use_container_width=True)
    
    with col2:
        # Sum of Profit by Category
        st.subheader("Profit by Product Category")
        category_profit = px.pie(filtered_profit.groupby("Category")["Profit"].sum(), values='Profit', names=filtered_profit.groupby("Category")["Profit"].sum().index, color_discrete_sequence=colour_palete)
        st.plotly_chart(category_profit, use_container_width=True)

    # Sum of Profit by Market
    st.subheader("Profit by Market")
    market_profit = filtered_profit.groupby("Market")["Profit"].sum()
    st.bar_chart(market_profit, color='#357b72')

    # Create the scatter plot with customized background color
    plt.figure(figsize=(8,6), facecolor='#E8E8E8')
    sns.set_style("white")  # Remove grid lines
    plt.rcParams['axes.facecolor'] = '#E8E8E8'  # Set background color
    sns.scatterplot(data=filtered_profit, x="Discount", y="Profit", color='#357b72')
    # Display the plot
    st.pyplot(plt)

#PRODUCT INSIGHTS
elif selected_option == "Product Insights":
    # Define color palette
    color_palette_1 = ['#001524', '#0E2A40', '#445D48', '#5F6F52', '#7A856C', '#A9B388', '#C8C9A8', '#D6CC99', '#FDE5D4', '#FEFAE0']
    color_palette_2 = ['#294B29', '#4F6F52', '#50623A', '#739072', '#789461', '#86A789', '#A9B388', '#C8C9A8', '#DBE7C9', '#D2E3C8']
    color_palette_3 = ['#00425A', '#1F8A70', '#2E9E7E', '#3FB28E', '#4FBDA0', '#5FC8B2', '#6FD3C4', '#7FDAE6', '#8FE5F8', '#9FF0FF']
    color_palette_4 = ['#7AA874', '#88B78D', '#98D8AA', '#A9E9B7', '#C3EDC0','#E9FFC2', '#F3E99F', '#F7DB6A', '#EBB02D', '#D864A9']
    

    # Calculate highest sales, highest profit, top 10 purchased products, and least 10 purchased products
    highest_sales_products = df.groupby("Product Name")["Sales"].sum().nlargest(10)
    highest_profit_products = df.groupby("Product Name")["Profit"].sum().nlargest(10)
    top_10_purchased_products = df["Product Name"].value_counts().nlargest(10)
    least_10_purchased_products = df["Product Name"].value_counts().nsmallest(10)

    # Create bar charts for each metric
    st.subheader("Products with Highest Sales")
    highest_sales_chart = px.bar(highest_sales_products, x=highest_sales_products.index, y="Sales", color=highest_sales_products.index, color_discrete_sequence=color_palette_1)
    st.plotly_chart(highest_sales_chart, use_container_width=True)

    st.subheader("Products with Highest Profit")
    highest_profit_chart = px.bar(highest_profit_products, x=highest_profit_products.index, y="Profit", color=highest_profit_products.index, color_discrete_sequence=color_palette_2)
    st.plotly_chart(highest_profit_chart, use_container_width=True)

    st.subheader("Top 10 Purchased Products")
    top_10_purchased_chart = px.bar(top_10_purchased_products, x=top_10_purchased_products.index, y=top_10_purchased_products.values, color=top_10_purchased_products.index, color_discrete_sequence=color_palette_3)
    st.plotly_chart(top_10_purchased_chart, use_container_width=True)

    st.subheader("Least 10 Purchased Products")
    least_10_purchased_chart = px.bar(least_10_purchased_products, x=least_10_purchased_products.index, y=least_10_purchased_products.values, color=least_10_purchased_products.index, color_discrete_sequence=color_palette_4)
    st.plotly_chart(least_10_purchased_chart, use_container_width=True)
