import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils.styling import kpi_metric, card, info_banner, stat_row

def show_dashboard():
    """Display the main dashboard with KPIs and charts"""
    
    # User info banner
    info_banner("You have full access to all dashboard features and data")
    
    # Load data
    sales_df = pd.read_csv('data/sales.csv')
    inventory_df = pd.read_csv('data/inventory.csv')
    purchases_df = pd.read_csv('data/purchases.csv')
    expenses_df = pd.read_csv('data/expenses.csv')
    
    # Convert date columns to datetime
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    purchases_df['date'] = pd.to_datetime(purchases_df['date'])
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    
    # Filter data for the last 30 days
    last_30_days = datetime.now() - timedelta(days=30)
    sales_last_30days = sales_df[sales_df['date'] >= last_30_days]
    
    # Calculate current month and previous month data for comparison
    current_month = sales_df['date'].dt.to_period('M').max()
    previous_month = current_month - 1
    
    sales_current_month = sales_df[sales_df['date'].dt.to_period('M') == current_month]
    sales_previous_month = sales_df[sales_df['date'].dt.to_period('M') == previous_month]
    
    # Calculate KPIs
    total_sales = sales_current_month['total_price'].sum()
    prev_sales = sales_previous_month['total_price'].sum()
    sales_change_percent = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    
    total_orders = len(sales_current_month)
    prev_orders = len(sales_previous_month)
    orders_change_percent = ((total_orders - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0
    
    total_customers = len(sales_current_month['customer_id'].unique())
    prev_customers = len(sales_previous_month['customer_id'].unique())
    customers_change_percent = ((total_customers - prev_customers) / prev_customers * 100) if prev_customers > 0 else 0
    
    avg_order_value = sales_current_month['total_price'].mean()
    prev_avg_order = sales_previous_month['total_price'].mean()
    aov_change_percent = ((avg_order_value - prev_avg_order) / prev_avg_order * 100) if prev_avg_order > 0 else 0
    
    conversion_rate = 3.5  # Example value
    prev_conversion = 3.0  # Example value
    conversion_change_percent = ((conversion_rate - prev_conversion) / prev_conversion * 100) if prev_conversion > 0 else 0
    
    revenue_growth = sales_change_percent
    
    # First row of KPIs
    st.markdown("<h2>Key Performance Indicators</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(kpi_metric(
            title="TOTAL SALES", 
            value=f"${total_sales:,.0f}" if total_sales > 1000 else f"${total_sales:,.2f}", 
            trend="up" if sales_change_percent > 0 else "down", 
            trend_value=f"{abs(sales_change_percent):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(kpi_metric(
            title="TOTAL ORDERS", 
            value=f"{total_orders}", 
            trend="up" if orders_change_percent > 0 else "down", 
            trend_value=f"{abs(orders_change_percent):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(kpi_metric(
            title="TOTAL CUSTOMERS", 
            value=f"{total_customers}", 
            trend="up" if customers_change_percent > 0 else "down", 
            trend_value=f"{abs(customers_change_percent):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    # Second row of KPIs
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(kpi_metric(
            title="AVERAGE ORDER VALUE", 
            value=f"${avg_order_value:.2f}", 
            trend="up" if aov_change_percent > 0 else "down", 
            trend_value=f"{abs(aov_change_percent):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(kpi_metric(
            title="CONVERSION RATE", 
            value=f"{conversion_rate}%", 
            trend="up" if conversion_change_percent > 0 else "down", 
            trend_value=f"{abs(conversion_change_percent):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(kpi_metric(
            title="REVENUE GROWTH", 
            value=f"{revenue_growth:.1f}%", 
            trend="up" if revenue_growth > 0 else "down", 
            trend_value=f"{abs(revenue_growth):.1f}% vs last month"), 
            unsafe_allow_html=True
        )
    
    # Charts row with sales overview
    st.markdown("<h2>Sales Overview</h2>", unsafe_allow_html=True)
    
    # Charts with better styling
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Create the Monthly Sales chart
        monthly_sales = sales_df.set_index('date').resample('ME')['total_price'].sum().reset_index()
        monthly_sales['month'] = monthly_sales['date'].dt.strftime('%b')
        
        fig1 = px.bar(
            monthly_sales.tail(12),
            x='month',
            y='total_price',
            labels={'month': '', 'total_price': 'Revenue ($)'},
            title='Monthly Sales Revenue'
        )
        
        fig1.update_traces(marker_color='#3498db', marker_line_color='#2980b9', 
                          marker_line_width=1.5, opacity=0.8)
        fig1.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'},
                'x': 0.05,
                'xanchor': 'left',
                'y': 0.95
            },
            margin=dict(l=20, r=20, t=50, b=30),
            xaxis=dict(
                showgrid=True,
                gridcolor='#f0f0f0',
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#f0f0f0',
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d'),
                tickprefix='$',
                title='Revenue ($)'
            ),
            height=400,
            width=None,
            bargap=0.2
        )
        
        # Add a trend line
        monthly_revenue = monthly_sales.tail(12)['total_price']
        x = list(range(len(monthly_revenue)))
        
        trend_line = np.polyfit(x, monthly_revenue, 1)
        trend_fn = np.poly1d(trend_line)
        trend_values = trend_fn(x)
        
        fig1.add_trace(go.Scatter(
            x=monthly_sales.tail(12)['month'],
            y=trend_values,
            mode='lines',
            name='Trend',
            line=dict(color='#e74c3c', width=3, dash='dot'),
        ))
        
        st.plotly_chart(fig1, use_container_width=True)
        
    with chart_col2:
        # Create daily sales trend chart
        daily_sales = sales_last_30days.set_index('date').resample('D')['total_price'].sum().reset_index()
        daily_sales = daily_sales.tail(15)  # Last 15 days for better visibility
        
        fig2 = px.line(
            daily_sales,
            x='date',
            y='total_price',
            labels={'date': '', 'total_price': 'Revenue ($)'},
            title='Daily Sales Trend (Last 15 Days)'
        )
        
        fig2.update_traces(line=dict(color='#2ecc71', width=3), 
                          mode='lines+markers',
                          marker=dict(size=8, color='#27ae60'))
        fig2.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'},
                'x': 0.05,
                'xanchor': 'left',
                'y': 0.95
            },
            margin=dict(l=20, r=20, t=50, b=30),
            xaxis=dict(
                showgrid=True,
                gridcolor='#f0f0f0',
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d'),
                tickformat='%b %d'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#f0f0f0',
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d'),
                tickprefix='$',
                title='Revenue ($)'
            ),
            height=400,
            width=None
        )
        
        # Add a moving average line
        window_size = 3
        daily_sales['moving_avg'] = daily_sales['total_price'].rolling(window=window_size, min_periods=1).mean()
        
        fig2.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['moving_avg'],
            mode='lines',
            name=f'{window_size}-Day Moving Avg',
            line=dict(color='#f39c12', width=2, dash='solid'),
        ))
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Additional data insights
    st.markdown("<h2>Business Insights</h2>", unsafe_allow_html=True)
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        # Payment methods distribution
        payment_counts = sales_df['payment_method'].value_counts().reset_index()
        payment_counts.columns = ['method', 'count']
        payment_counts['percentage'] = (payment_counts['count'] / payment_counts['count'].sum() * 100).round(1)
        
        fig3 = px.pie(
            payment_counts,
            values='count',
            names='method',
            title='Payment Methods',
            hole=0.4,
            color_discrete_sequence=['#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#1abc9c']
        )
        
        fig3.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'},
                'x': 0.05,
                'xanchor': 'left',
                'y': 0.95
            },
            margin=dict(l=20, r=20, t=50, b=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(family='Arial, sans-serif', size=12, color='#7f8c8d')
            ),
            height=400,
            width=None,
            annotations=[
                dict(
                    text='Payment<br>Methods',
                    x=0.5, y=0.5,
                    font_size=16,
                    font_family='Arial, sans-serif',
                    font_color='#2c3e50',
                    showarrow=False
                )
            ]
        )
        
        st.plotly_chart(fig3, use_container_width=True)
        
    with insight_col2:
        # Product categories and sales
        category_sales = sales_df.groupby('category')['total_price'].sum().sort_values(ascending=False).reset_index()
        
        fig4 = px.bar(
            category_sales,
            x='total_price',
            y='category',
            labels={'total_price': 'Total Revenue ($)', 'category': ''},
            title='Sales by Product Category',
            orientation='h',
            color='total_price',
            color_continuous_scale='Blues'
        )
        
        fig4.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial, sans-serif'},
                'x': 0.05,
                'xanchor': 'left',
                'y': 0.95
            },
            margin=dict(l=20, r=20, t=50, b=30),
            xaxis=dict(
                showgrid=True,
                gridcolor='#f0f0f0',
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d'),
                tickprefix='$'
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(family='Arial, sans-serif', size=12, color='#7f8c8d'),
                title=None,
                autorange="reversed"  # To have highest value at the top
            ),
            height=400,
            width=None,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # Third row with additional cards
    st.markdown("<h2>Business Health</h2>", unsafe_allow_html=True)
    card_col1, card_col2, card_col3 = st.columns(3)
    
    with card_col1:
        # Top selling products
        top_products = sales_df.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(5)
        
        top_products_html = ""
        for product, quantity in top_products.items():
            top_products_html += stat_row(product, f"{quantity} units")
        
        st.markdown(card("Top Selling Products", top_products_html), unsafe_allow_html=True)
        
    with card_col2:
        # Inventory status
        low_stock_count = len(inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_level']])
        out_of_stock = len(inventory_df[inventory_df['current_stock'] == 0])
        total_inventory_value = inventory_df['total_value'].sum()
        avg_inventory_level = inventory_df['current_stock'].mean()
        
        inventory_stats_html = ""
        inventory_stats_html += stat_row("Low Stock Items", f"{low_stock_count} products", icon="⚠️", value_color="#f39c12")
        inventory_stats_html += stat_row("Out of Stock", f"{out_of_stock} products", icon="❌", value_color="#e74c3c")
        inventory_stats_html += stat_row("Total Inventory Value", f"${total_inventory_value:,.2f}", icon="💰")
        inventory_stats_html += stat_row("Average Stock Level", f"{avg_inventory_level:.1f} units", icon="📊")
        
        st.markdown(card("Inventory Overview", inventory_stats_html), unsafe_allow_html=True)
        
    with card_col3:
        # Recent activity
        latest_sales = sales_df.sort_values('date', ascending=False).head(4)
        
        activity_html = ""
        for _, sale in latest_sales.iterrows():
            date_str = pd.to_datetime(sale['date']).strftime('%b %d')
            activity_html += stat_row(
                f"{date_str}: {sale['product_name']}", 
                f"${sale['total_price']:.2f}"
            )
        
        st.markdown(card("Recent Sales Activity", activity_html), unsafe_allow_html=True) 