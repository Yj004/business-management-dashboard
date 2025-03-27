import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.styling import kpi_metric

def show_purchase():
    """Display the purchase dashboard with KPIs and charts"""
    
    st.header("Purchase Management")
    
    # Load data
    purchases_df = pd.read_csv('data/purchases.csv')
    inventory_df = pd.read_csv('data/inventory.csv')
    
    # Convert date column to datetime
    purchases_df['date'] = pd.to_datetime(purchases_df['date'])
    
    # Filter data
    current_month = datetime.now().replace(day=1)
    previous_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_month_purchases = purchases_df[purchases_df['date'] >= current_month]
    previous_month_purchases = purchases_df[(purchases_df['date'] >= previous_month) & (purchases_df['date'] < current_month)]
    
    # Calculate KPIs
    total_purchase_value = current_month_purchases['total_cost'].sum()
    prev_purchase_value = previous_month_purchases['total_cost'].sum()
    purchase_change_percent = ((total_purchase_value - prev_purchase_value) / prev_purchase_value * 100) if prev_purchase_value > 0 else 0
    
    total_purchase_count = len(current_month_purchases)
    prev_purchase_count = len(previous_month_purchases)
    purchase_count_change = ((total_purchase_count - prev_purchase_count) / prev_purchase_count * 100) if prev_purchase_count > 0 else 0
    
    # Orders by status
    pending_orders = current_month_purchases[current_month_purchases['status'] == 'Pending']
    pending_count = len(pending_orders)
    pending_value = pending_orders['total_cost'].sum()
    
    ordered_orders = current_month_purchases[current_month_purchases['status'] == 'Ordered']
    ordered_count = len(ordered_orders)
    
    delivered_orders = current_month_purchases[current_month_purchases['status'] == 'Delivered']
    delivered_count = len(delivered_orders)
    
    avg_purchase_value = current_month_purchases['total_cost'].mean() if len(current_month_purchases) > 0 else 0
    
    # KPI Row
    st.markdown("<h3 style='text-align: center;'>Purchase Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_metric("Total Purchase Value", f"${total_purchase_value:,.2f}", trend="up" if purchase_change_percent > 0 else "down", trend_value=f"{abs(purchase_change_percent):.1f}%"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_metric("Purchase Orders", f"{total_purchase_count}", trend="up" if purchase_count_change > 0 else "down", trend_value=f"{abs(purchase_count_change):.1f}%"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_metric("Average Order Value", f"${avg_purchase_value:.2f}"), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(kpi_metric("Pending Orders", f"{pending_count} (${pending_value:,.2f})"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_metric("Ordered", f"{ordered_count}"), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_metric("Delivered", f"{delivered_count}"), unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("<h3 style='text-align: center;'>Purchase Analysis</h3>", unsafe_allow_html=True)
    
    # Chart 1: Monthly Purchase Trend
    # Group by month and calculate total purchase value
    purchases_df['month'] = purchases_df['date'].dt.to_period('M')
    monthly_purchases = purchases_df.groupby(purchases_df['month'].astype(str))['total_cost'].sum().reset_index()
    
    # Get the last 6 months for better visualization
    monthly_purchases = monthly_purchases.tail(6)
    
    fig1 = px.bar(
        monthly_purchases,
        x='month',
        y='total_cost',
        title='Monthly Purchase Value',
        labels={'month': 'Month', 'total_cost': 'Purchase Value ($)'},
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
    
    # Chart 2: Purchase by Category
    purchase_by_category = purchases_df.groupby('category')[['quantity', 'total_cost']].sum().reset_index()
    
    fig2 = px.bar(
        purchase_by_category,
        x='category',
        y='total_cost',
        title='Purchase Value by Category',
        color='quantity',
        labels={'total_cost': 'Total Cost ($)', 'category': 'Product Category', 'quantity': 'Quantity'},
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
    
    # Chart 3: Purchase Status Distribution
    status_counts = purchases_df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    fig3 = px.pie(
        status_counts,
        values='count',
        names='status',
        title='Purchase Orders by Status',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig3.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    # Chart 4: Supplier Distribution
    supplier_purchases = purchases_df.groupby('supplier_id')['total_cost'].sum().reset_index()
    supplier_purchases = supplier_purchases.sort_values('total_cost', ascending=False)
    supplier_purchases['supplier_name'] = "Supplier " + supplier_purchases['supplier_id'].astype(str)
    
    fig4 = px.bar(
        supplier_purchases,
        x='supplier_name',
        y='total_cost',
        title='Purchase Value by Supplier',
        labels={'supplier_name': 'Supplier', 'total_cost': 'Purchase Value ($)'},
        template='plotly_white',
        color='total_cost',
        color_continuous_scale='Viridis'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
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
    
    # Recent Purchase Orders
    st.markdown("<h3 style='text-align: center;'>Recent Purchase Orders</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Recent Orders", "Pending Orders", "Create New Order"])
    
    with tab1:
        recent_orders = purchases_df.sort_values('date', ascending=False).head(10)
        st.dataframe(
            recent_orders[['date', 'product_name', 'category', 'quantity', 'unit_cost', 'total_cost', 'status']],
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        pending_orders = purchases_df[purchases_df['status'] == 'Pending'].sort_values('date', ascending=False)
        if not pending_orders.empty:
            st.dataframe(
                pending_orders[['date', 'product_name', 'category', 'quantity', 'unit_cost', 'total_cost']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No pending orders.")
    
    with tab3:
        # Create a form for new purchase order
        with st.form("new_purchase_order"):
            st.markdown("#### Create New Purchase Order")
            
            # Form fields
            product = st.selectbox("Product", options=inventory_df['product_name'].tolist())
            quantity = st.number_input("Quantity", min_value=1, value=10)
            supplier = st.selectbox("Supplier", options=[f"Supplier {i}" for i in range(1, 11)])
            
            # Get product details
            product_details = inventory_df[inventory_df['product_name'] == product].iloc[0]
            unit_cost = st.number_input("Unit Cost", value=float(product_details['unit_cost']))
            
            total_cost = quantity * unit_cost
            
            st.write(f"Total Cost: ${total_cost:,.2f}")
            
            # Submit button
            submitted = st.form_submit_button("Create Purchase Order")
            
            if submitted:
                st.success(f"Purchase order created for {quantity} units of {product} from {supplier}.")
                st.balloons() 