import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styling import kpi_metric

def show_inventory():
    """Display the inventory dashboard with KPIs and charts"""
    
    st.header("Inventory Management")
    
    # Load inventory data
    inventory_df = pd.read_csv('data/inventory.csv')
    sales_df = pd.read_csv('data/sales.csv')
    purchases_df = pd.read_csv('data/purchases.csv')
    
    # Convert dates
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    # Calculate KPIs
    total_items = inventory_df['current_stock'].sum()
    total_value = inventory_df['total_value'].sum()
    avg_item_cost = total_value / total_items if total_items > 0 else 0
    
    # Low stock items
    low_stock_items = inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_level']]
    low_stock_count = len(low_stock_items)
    
    # Out of stock items
    out_of_stock = inventory_df[inventory_df['current_stock'] == 0]
    out_of_stock_count = len(out_of_stock)
    
    # Calculate stock turnover ratio (using last 30 days of sales)
    last_30_days_sales = sales_df[sales_df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=30))]
    sales_by_product = last_30_days_sales.groupby('product_id')['quantity'].sum().reset_index()
    
    # Merge with inventory to calculate turnover
    inventory_with_sales = inventory_df.merge(sales_by_product, left_on='product_id', right_on='product_id', how='left')
    inventory_with_sales['quantity'] = inventory_with_sales['quantity'].fillna(0)
    inventory_with_sales['turnover_ratio'] = inventory_with_sales['quantity'] / inventory_with_sales['current_stock']
    avg_turnover = inventory_with_sales['turnover_ratio'].mean()
    
    # KPI Row
    st.markdown("<h3 style='text-align: center;'>Inventory Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_metric("Total Stock Items", f"{int(total_items):,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_metric("Total Inventory Value", f"${total_value:,.2f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_metric("Average Item Cost", f"${avg_item_cost:.2f}"), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(kpi_metric("Low Stock Items", f"{low_stock_count}", trend="down" if low_stock_count > 0 else None), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_metric("Out of Stock Items", f"{out_of_stock_count}", trend="down" if out_of_stock_count > 0 else None), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_metric("Avg Stock Turnover (30d)", f"{avg_turnover:.2f}"), unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("<h3 style='text-align: center;'>Inventory Analysis</h3>", unsafe_allow_html=True)
    
    # Chart 1: Inventory Levels by Category
    inventory_by_category = inventory_df.groupby('category')[['current_stock', 'total_value']].sum().reset_index()
    
    fig1 = px.bar(
        inventory_by_category,
        x='category',
        y='current_stock',
        title='Inventory Levels by Category',
        color='total_value',
        labels={'current_stock': 'Stock Quantity', 'category': 'Product Category', 'total_value': 'Value ($)'},
        template='plotly_white',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 2: Stock vs Reorder Level
    # Select top 10 items by value for readability
    top_value_items = inventory_df.sort_values('total_value', ascending=False).head(10)
    
    fig2 = px.bar(
        top_value_items,
        x='product_name',
        y=['current_stock', 'reorder_level'],
        title='Current Stock vs. Reorder Level (Top 10 items by value)',
        labels={'value': 'Quantity', 'product_name': 'Product', 'variable': 'Metric'},
        template='plotly_white',
        barmode='group',
        color_discrete_map={'current_stock': '#1E3A8A', 'reorder_level': '#dc3545'}
    )
    fig2.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=50),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Chart 3: Inventory Value Distribution by Category
    fig3 = px.pie(
        inventory_by_category,
        values='total_value',
        names='category',
        title='Inventory Value Distribution by Category',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig3.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    # Chart 4: Turnover Ratio (Stock Velocity)
    # Get top 10 items by turnover ratio
    inventory_with_sales_nonzero = inventory_with_sales[inventory_with_sales['current_stock'] > 0]
    top_turnover = inventory_with_sales_nonzero.sort_values('turnover_ratio', ascending=False).head(10)
    
    fig4 = px.bar(
        top_turnover,
        x='product_name',
        y='turnover_ratio',
        title='Stock Turnover Ratio - Top 10 Products',
        labels={'turnover_ratio': 'Turnover Ratio (30 days)', 'product_name': 'Product'},
        template='plotly_white',
        color='turnover_ratio',
        color_continuous_scale='Viridis'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=50),
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
    
    # Additional section: Low stock items table
    st.markdown("<h3 style='text-align: center;'>Inventory Management</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Low Stock Items", "All Inventory", "Stock Movement"])
    
    with tab1:
        if not low_stock_items.empty:
            st.markdown("#### Items Requiring Restock")
            st.dataframe(
                low_stock_items[['product_name', 'category', 'current_stock', 'reorder_level', 'unit_cost', 'total_value']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No items below reorder level.")
    
    with tab2:
        st.markdown("#### Complete Inventory List")
        st.dataframe(
            inventory_df[['product_name', 'category', 'current_stock', 'reorder_level', 'unit_cost', 'total_value', 'last_restocked']],
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.markdown("#### Recent Stock Movements")
        recent_purchases = purchases_df.sort_values('date', ascending=False).head(10)
        st.dataframe(
            recent_purchases[['date', 'product_name', 'quantity', 'unit_cost', 'total_cost', 'status']],
            use_container_width=True,
            hide_index=True
        ) 