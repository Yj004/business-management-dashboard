import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.styling import kpi_metric

def show_sales():
    """Display the sales dashboard with KPIs and charts"""
    
    st.header("Sales Management")
    
    # Load data
    sales_df = pd.read_csv('data/sales.csv')
    
    # Convert date column to datetime
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Filter data for different time periods
    current_date = datetime.now()
    current_month_start = current_date.replace(day=1)
    previous_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    
    current_month_sales = sales_df[sales_df['date'] >= current_month_start]
    previous_month_sales = sales_df[(sales_df['date'] >= previous_month_start) & (sales_df['date'] < current_month_start)]
    
    # Calculate KPIs
    total_revenue = current_month_sales['total_price'].sum()
    prev_revenue = previous_month_sales['total_price'].sum()
    revenue_change_percent = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    total_profit = current_month_sales['profit'].sum()
    prev_profit = previous_month_sales['profit'].sum()
    profit_change_percent = ((total_profit - prev_profit) / prev_profit * 100) if prev_profit > 0 else 0
    
    total_orders = len(current_month_sales.groupby(['date', 'customer_id']))
    prev_orders = len(previous_month_sales.groupby(['date', 'customer_id']))
    orders_change_percent = ((total_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    
    avg_order_value = current_month_sales['total_price'].mean()
    prev_avg_order = previous_month_sales['total_price'].mean()
    aov_change_percent = ((avg_order_value - prev_avg_order) / prev_avg_order * 100) if prev_avg_order > 0 else 0
    
    total_units_sold = current_month_sales['quantity'].sum()
    prev_units_sold = previous_month_sales['quantity'].sum()
    units_change_percent = ((total_units_sold - prev_units_sold) / prev_units_sold * 100) if prev_units_sold > 0 else 0
    
    # Calculate profit margin
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    prev_profit_margin = (prev_profit / prev_revenue * 100) if prev_revenue > 0 else 0
    margin_change_percent = (profit_margin - prev_profit_margin)
    
    # KPI Row
    st.markdown("<h3 style='text-align: center;'>Sales Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_metric("Total Revenue", f"${total_revenue:,.2f}", trend="up" if revenue_change_percent > 0 else "down", trend_value=f"{abs(revenue_change_percent):.1f}%"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_metric("Total Profit", f"${total_profit:,.2f}", trend="up" if profit_change_percent > 0 else "down", trend_value=f"{abs(profit_change_percent):.1f}%"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_metric("Profit Margin", f"{profit_margin:.1f}%", trend="up" if margin_change_percent > 0 else "down", trend_value=f"{abs(margin_change_percent):.1f}%"), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(kpi_metric("Total Orders", f"{total_orders}", trend="up" if orders_change_percent > 0 else "down", trend_value=f"{abs(orders_change_percent):.1f}%"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_metric("Average Order Value", f"${avg_order_value:.2f}", trend="up" if aov_change_percent > 0 else "down", trend_value=f"{abs(aov_change_percent):.1f}%"), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_metric("Units Sold", f"{int(total_units_sold)}", trend="up" if units_change_percent > 0 else "down", trend_value=f"{abs(units_change_percent):.1f}%"), unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("<h3 style='text-align: center;'>Sales Analysis</h3>", unsafe_allow_html=True)
    
    # Time filter for charts
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 12 Months", "All Time"],
        index=1
    )
    
    if time_period == "Last 7 Days":
        filter_date = current_date - timedelta(days=7)
    elif time_period == "Last 30 Days":
        filter_date = current_date - timedelta(days=30)
    elif time_period == "Last 90 Days":
        filter_date = current_date - timedelta(days=90)
    elif time_period == "Last 12 Months":
        filter_date = current_date - timedelta(days=365)
    else:
        filter_date = sales_df['date'].min()
    
    filtered_sales = sales_df[sales_df['date'] >= filter_date]
    
    # Chart 1: Daily Sales Trend
    if time_period in ["Last 7 Days", "Last 30 Days"]:
        # For shorter periods, show daily trends
        daily_sales = filtered_sales.groupby(filtered_sales['date'].dt.date)['total_price'].sum().reset_index()
        
        fig1 = px.line(
            daily_sales, 
            x='date', 
            y='total_price',
            title='Daily Sales Revenue',
            labels={'date': 'Date', 'total_price': 'Revenue ($)'},
            template='plotly_white'
        )
        fig1.update_traces(mode='lines+markers', line=dict(color='#1E3A8A', width=3))
    else:
        # For longer periods, show monthly trends
        filtered_sales['month'] = filtered_sales['date'].dt.to_period('M')
        monthly_sales = filtered_sales.groupby(filtered_sales['month'].astype(str))['total_price'].sum().reset_index()
        
        fig1 = px.bar(
            monthly_sales, 
            x='month', 
            y='total_price',
            title='Monthly Sales Revenue',
            labels={'month': 'Month', 'total_price': 'Revenue ($)'},
            template='plotly_white',
            color_discrete_sequence=['#1E3A8A']
        )
    
    fig1.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 2: Sales by Category
    category_sales = filtered_sales.groupby('category')[['total_price', 'profit']].sum().reset_index()
    category_sales = category_sales.sort_values('total_price', ascending=False)
    
    fig2 = px.bar(
        category_sales,
        x='category',
        y='total_price',
        title='Sales by Product Category',
        color='profit',
        labels={'total_price': 'Revenue ($)', 'category': 'Product Category', 'profit': 'Profit ($)'},
        template='plotly_white',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 3: Payment Method Distribution
    payment_counts = filtered_sales['payment_method'].value_counts().reset_index()
    payment_counts.columns = ['payment_method', 'count']
    
    fig3 = px.pie(
        payment_counts,
        values='count',
        names='payment_method',
        title='Sales by Payment Method',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig3.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    # Chart 4: Top Products
    product_sales = filtered_sales.groupby(['product_id', 'product_name'])['total_price'].sum().reset_index()
    top_products = product_sales.sort_values('total_price', ascending=False).head(10)
    
    fig4 = px.bar(
        top_products,
        y='product_name',
        x='total_price',
        title='Top 10 Products by Sales',
        labels={'product_name': 'Product', 'total_price': 'Revenue ($)'},
        template='plotly_white',
        color='total_price',
        color_continuous_scale='Viridis',
        orientation='h'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        yaxis=dict(showgrid=False),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Arrange charts in a 2x2 grid
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.plotly_chart(fig1, use_container_width=True)
    with chart_col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        st.plotly_chart(fig3, use_container_width=True)
    with chart_col4:
        st.plotly_chart(fig4, use_container_width=True)
    
    # Sales records table
    st.markdown("<h3 style='text-align: center;'>Sales Records</h3>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Recent Sales", "Sales by Product"])
    
    with tab1:
        recent_sales = sales_df.sort_values('date', ascending=False).head(20)
        st.dataframe(
            recent_sales[['date', 'product_name', 'category', 'quantity', 'unit_price', 'total_price', 'profit', 'payment_method']],
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        product_summary = sales_df.groupby(['product_id', 'product_name', 'category'])[['quantity', 'total_price', 'profit']].sum().reset_index()
        product_summary['profit_margin'] = (product_summary['profit'] / product_summary['total_price'] * 100).round(1)
        product_summary = product_summary.sort_values('total_price', ascending=False)
        
        st.dataframe(
            product_summary[['product_name', 'category', 'quantity', 'total_price', 'profit', 'profit_margin']],
            use_container_width=True,
            hide_index=True,
            column_config={
                'total_price': st.column_config.NumberColumn(
                    'Revenue ($)',
                    format="$%.2f",
                ),
                'profit': st.column_config.NumberColumn(
                    'Profit ($)',
                    format="$%.2f",
                ),
                'profit_margin': st.column_config.NumberColumn(
                    'Margin (%)',
                    format="%.1f%%",
                ),
            }
        ) 