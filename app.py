#Import Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

# Load the dataset
df = pd.read_excel("Superstore.xlsx")

# Set Streamlit app title
st.title("Minger Dashboard")

# Create a sidebar with tiles
with st.sidebar:
    st.sidebar.header("Analysis Focus")
    selected_option = st.radio("Select an option:", ["Sales Analysis", "Profit Analysis", "Product Insights"])
 
    # Filter by date range
    st.sidebar.subheader("Date Range Filter")
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime(df["Order Date"]).min(), min_value=pd.to_datetime(df["Order Date"]).min(), max_value=pd.to_datetime(df["Order Date"]).max())
    end_date = st.sidebar.date_input("End Date", pd.to_datetime(df["Order Date"]).max(), min_value=pd.to_datetime(df["Order Date"]).min(), max_value=pd.to_datetime(df["Order Date"]).max())

    # Filter by Region
    st.sidebar.subheader("Region Filter")
    all_regions = ["All"] + list(df["Region"].unique())
    selected_region = st.sidebar.selectbox("Select Region", all_regions)
    
    # Filter by Country based on selected region
    countries = df[df["Region"] == selected_region]["Country"].unique() if selected_region != "All" else df["Country"].unique()
    st.sidebar.subheader("Country Filter")
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + list(countries))

    # Filter by State based on selected country
    states = df[df["Country"] == selected_country]["State"].unique() if selected_country != "All" else df["State"].unique()
    st.sidebar.subheader("State Filter")
    selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))
    
    # Filter by Sub-Category
    st.sidebar.subheader("Sub-Category Filter")
    all_sub_categories = ["All"] + list(df["Sub-Category"].unique())
    selected_sub_category = st.sidebar.selectbox("Select Sub-Category", all_sub_categories)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

#Colour palette
colour_palette=['#357b72', '#6b9b8e', '#99bcb5', '#c8dedb']

# Filter options
if selected_option == "Sales Analysis":
    st.header("Sales Analysis")
    # Convert start_date and end_date to Pandas Timestamp objects
    filtered_sales = df[
        (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date) &
        (df["Region"] if selected_region == "All" else df["Region"] == selected_region) &
        (df["Country"] if selected_country == "All" else df["Country"] == selected_country) &
        (df["State"] if selected_state == "All" else df["State"] == selected_state) &
        (df["Sub-Category"] if selected_sub_category == "All" else df["Sub-Category"] == selected_sub_category)]
    
    # Create columns for layout
    col1, col2, col3 = st.columns(3)

    # Calculate KPIs and round to the nearest whole number as per the format
    total_sales = "${:,.0f}".format(round(filtered_sales["Sales"].sum()))
    total_quantity = "{:,.0f} units".format(round(filtered_sales["Quantity"].sum())) 
    total_profit = "${:,.0f}".format(round(filtered_sales["Profit"].sum()))

    # Display KPIs in separate columns
    with col1:
        st.metric("Total Sales", total_sales)

    with col2:
        st.metric("Total Quantity", total_quantity)

    with col3:
        st.metric("Total Profit", total_profit)

    #Sales Trend
    st.subheader("Sales Trend Over Time")
    st.line_chart(filtered_sales.set_index("Order Date")["Sales"], color='#357b72', use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sales by Segment")
        segment_sales = px.pie(filtered_sales.groupby("Segment")["Sales"].sum(), values='Sales', names=filtered_sales.groupby("Segment")["Sales"].sum().index, color_discrete_sequence=colour_palette)
        st.plotly_chart(segment_sales, use_container_width=True)
        
    with col2:
        st.subheader("Sales by Category")
        category_sales = px.pie(filtered_sales.groupby("Category")["Sales"].sum(), values='Sales', names=filtered_sales.groupby("Category")["Sales"].sum().index, color_discrete_sequence=colour_palette)
        st.plotly_chart(category_sales, use_container_width=True)
   
    # Sum of Sales by Market
    st.subheader("Sales by Market")
    market_sales = filtered_sales.groupby("Market")["Sales"].sum()
    st.bar_chart(market_sales, color='#357b72')

    # Create the scatter plot with customized background color
    st.subheader("Relationship between Sales and Discount")
    plt.figure(figsize=(8,5), facecolor='#FFFFFF')
    sns.set_style("white")  # Remove grid lines
    plt.rcParams['axes.facecolor'] = '#FFFFFF'  # Set background color
    sns.scatterplot(data=filtered_sales, x="Discount", y="Sales", color='#357b72')
    # Display the plot
    st.pyplot(plt)

elif selected_option == "Profit Analysis":
    st.header("Profit Analysis")
    filtered_profit = df[
        (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date) &
        (df["Region"] if selected_region == "All" else df["Region"] == selected_region) &
        (df["Country"] if selected_country == "All" else df["Country"] == selected_country) &
        (df["State"] if selected_state == "All" else df["State"] == selected_state) &
        (df["Sub-Category"] if selected_sub_category == "All" else df["Sub-Category"] == selected_sub_category)]

    # Create columns for layout
    col1, col2, col3 = st.columns(3)

    # Calculate KPIs and round to the nearest whole number as per the format
    total_sales = "${:,.0f}".format(round(filtered_profit["Sales"].sum()))
    total_quantity = "{:,.0f} units".format(round(filtered_profit["Quantity"].sum()))
    total_profit = "${:,.0f}".format(round(filtered_profit["Profit"].sum()))

    # Display KPIs in separate columns
    with col1:
        st.metric("Total Sales", total_sales)

    with col2:
        st.metric("Total Quantity", total_quantity)

    with col3:
        st.metric("Total Profit", total_profit)

    #Profit Trend
    st.subheader("Profit Trend over Time")
    st.line_chart(filtered_profit.set_index("Order Date")["Profit"], color='#357b72')

    # Sum of Sales by Segment and by Category
    # Create columns for layout
    col1, col2 = st.columns(2)
    with col1:   
        # Sum of Profit by Segment
        st.subheader("Profit by Segment")
        segment_profit = px.pie(filtered_profit.groupby("Segment")["Profit"].sum(), values='Profit', names=filtered_profit.groupby("Segment")["Profit"].sum().index, color_discrete_sequence=colour_palette)
        st.plotly_chart(segment_profit, use_container_width=True)
    
    with col2:
        # Sum of Profit by Category
        st.subheader("Profit by Product Category")
        category_profit = px.pie(filtered_profit.groupby("Category")["Profit"].sum(), values='Profit', names=filtered_profit.groupby("Category")["Profit"].sum().index, color_discrete_sequence=colour_palette)
        st.plotly_chart(category_profit, use_container_width=True)

    # Sum of Profit by Market
    st.subheader("Profit by Market")
    market_profit = filtered_profit.groupby("Market")["Profit"].sum()
    st.bar_chart(market_profit, color='#357b72')

    # Create the scatter plot with customized background color
    st.subheader("Relationship between Profit and Discount")
    plt.figure(figsize=(8,5), facecolor='#FFFFFF')
    sns.set_style("white")  # Remove grid lines
    plt.rcParams['axes.facecolor'] = '#FFFFFF'  # Set background color
    sns.scatterplot(data=filtered_profit, x="Discount", y="Profit", color='#357b72')
    # Display the plot
    st.pyplot(plt)

#PRODUCT INSIGHTS
elif selected_option == "Product Insights":
    st.header("Product Insights")
    # Define color palette
    color_palette_1 = ['#001524', '#0E2A40', '#445D48', '#5F6F52', '#7A856C', '#A9B388', '#C8C9A8', '#D6CC99', '#FDE5D4', '#FEFAE0']
    color_palette_2 = ['#294B29', '#4F6F52', '#50623A', '#739072', '#789461', '#86A789', '#A9B388', '#C8C9A8', '#DBE7C9', '#D2E3C8']
    color_palette_3 = ['#00425A', '#1F8A70', '#2E9E7E', '#3FB28E', '#4FBDA0', '#5FC8B2', '#6FD3C4', '#7FDAE6', '#8FE5F8', '#9FF0FF']
    color_palette_4 = ['#7AA874', '#88B78D', '#98D8AA', '#A9E9B7', '#C3EDC0','#E9FFC2', '#F3E99F', '#F7DB6A', '#EBB02D', '#D864A9']
    
    # Apply filters
    filtered_products = df[
        (df["Order Date"] >= start_date) & (df["Order Date"] <= end_date) &
        (df["Region"] if selected_region == "All" else df["Region"] == selected_region) &
        (df["Country"] if selected_country == "All" else df["Country"] == selected_country) &
        (df["State"] if selected_state == "All" else df["State"] == selected_state) &
        (df["Sub-Category"] if selected_sub_category == "All" else df["Sub-Category"] == selected_sub_category)]
    
    # Create columns for layout
    col1, col2, col3 = st.columns(3)

    # Calculate KPIs and round to the nearest whole number as per the format
    total_sales = "${:,.0f}".format(round(filtered_products["Sales"].sum()))
    total_quantity = "{:,.0f} units".format(round(filtered_products["Quantity"].sum()))
    total_profit = "${:,.0f}".format(round(filtered_products["Profit"].sum()))

    # Display KPIs in separate columns
    with col1:
        st.metric("Total Sales", total_sales)

    with col2:
        st.metric("Total Quantity", total_quantity)

    with col3:
        st.metric("Total Profit", total_profit)

    # Calculate highest sales, highest profit, top 10 purchased products, and least 10 purchased products
    highest_sales_products = filtered_products.groupby("Product Name")["Sales"].sum().nlargest(10)
    highest_profit_products = filtered_products.groupby("Product Name")["Profit"].sum().nlargest(10)
    top_10_purchased_products = filtered_products["Product Name"].value_counts().nlargest(10)
    least_10_purchased_products = filtered_products["Product Name"].value_counts().nsmallest(10)

    # Create bar charts for each metric
    st.subheader("Products with Highest Sales")
    highest_sales_chart = px.bar(highest_sales_products, x=highest_sales_products.index, y="Sales", color=highest_sales_products.index, color_discrete_sequence=color_palette_1)
    st.plotly_chart(highest_sales_chart, use_container_width=True)

    st.subheader("Products with Highest Profit")
    highest_profit_chart = px.bar(highest_profit_products, x=highest_profit_products.index, y="Profit", color=highest_profit_products.index, color_discrete_sequence=color_palette_2)
    st.plotly_chart(highest_profit_chart, use_container_width=True)

    st.subheader("Top 10 Purchased Products")
    top_10_purchased_chart = px.bar(top_10_purchased_products, x=top_10_purchased_products.index, y=top_10_purchased_products.values, color=top_10_purchased_products.index, color_discrete_sequence=color_palette_3)
    top_10_purchased_chart.update_xaxes(title_text='Product Name')
    top_10_purchased_chart.update_yaxes(title_text='Number of Purchases')
    st.plotly_chart(top_10_purchased_chart, use_container_width=True)

    st.subheader("Least 10 Purchased Products")
    least_10_purchased_chart = px.bar(least_10_purchased_products, x=least_10_purchased_products.index, y=least_10_purchased_products.values, color=least_10_purchased_products.index, color_discrete_sequence=color_palette_4)
    least_10_purchased_chart.update_xaxes(title_text='Product Name')
    least_10_purchased_chart.update_yaxes(title_text='Number of Purchases')    
    st.plotly_chart(least_10_purchased_chart, use_container_width=True)

    #Market Basket Analysis obtained from the previous assessment
    # Convert 'Sub-Category' column into dummies
    transaction_df = pd.get_dummies(filtered_products['Sub-Category'])
    # Concatenate 'Order ID' column to transaction_df
    transaction_df = pd.concat([filtered_products['Order ID'], transaction_df], axis=1)
    # Group by 'Order ID' and aggregate to sum up the occurrence of each sub-category within each order
    transaction_df = transaction_df.groupby('Order ID').sum()
    # Convert all columns to binary values (1 if > 0, else 0)
    transaction_df = transaction_df.applymap(lambda x: 1 if x > 0 else 0)
    # Compute the co-occurrence matrix
    co_occurrence_matrix = transaction_df.T.dot(transaction_df)
    # Set diagonal elements to 0
    np.fill_diagonal(co_occurrence_matrix.values, 0)

    #Heatmap of Sub-categories
    st.subheader("Co-occurrence Matrix of Sub-Categories")
    # Plot the heatmap
    plt.figure(figsize=(10, 8), facecolor='#FFFFFF')
    sns.heatmap(co_occurrence_matrix, annot=True, cmap="YlGn", fmt="d", linewidths=2, color='#357b72')
    plt.title('Co-occurrence Matrix of Sub-Categories (Excluding Same Product Combinations)')
    plt.xlabel('Sub-Category')
    plt.ylabel('Sub-Category')
    # Show heatmap in Streamlit
    st.pyplot(plt)
    