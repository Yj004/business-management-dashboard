import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
from utils.styling import kpi_metric

def show_report():
    """Display the reporting dashboard with KPIs and charts"""
    
    st.header("Business Reports")
    
    # Load data
    sales_df = pd.read_csv('data/sales.csv')
    inventory_df = pd.read_csv('data/inventory.csv')
    purchases_df = pd.read_csv('data/purchases.csv')
    expenses_df = pd.read_csv('data/expenses.csv')
    performance_df = pd.read_csv('data/performance.csv')
    
    # Convert date columns to datetime
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    purchases_df['date'] = pd.to_datetime(purchases_df['date'])
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    performance_df['date'] = pd.to_datetime(performance_df['date'])
    
    # Time period filter
    report_period = st.selectbox(
        "Report Period",
        ["Current Month", "Previous Month", "Last 3 Months", "Last 6 Months", "Year to Date", "Last Year", "All Time"],
        index=0
    )
    
    # Set date filters based on selection
    current_date = datetime.now()
    current_month_start = current_date.replace(day=1)
    
    if report_period == "Current Month":
        start_date = current_month_start
        title_period = f"{current_date.strftime('%B %Y')}"
    elif report_period == "Previous Month":
        start_date = (current_month_start - timedelta(days=1)).replace(day=1)
        end_date = current_month_start - timedelta(days=1)
        title_period = f"{start_date.strftime('%B %Y')}"
    elif report_period == "Last 3 Months":
        start_date = (current_month_start - timedelta(days=90)).replace(day=1)
        title_period = f"{start_date.strftime('%B %Y')} - {current_date.strftime('%B %Y')}"
    elif report_period == "Last 6 Months":
        start_date = (current_month_start - timedelta(days=180)).replace(day=1)
        title_period = f"{start_date.strftime('%B %Y')} - {current_date.strftime('%B %Y')}"
    elif report_period == "Year to Date":
        start_date = current_date.replace(month=1, day=1)
        title_period = f"{current_date.year} YTD"
    elif report_period == "Last Year":
        start_date = current_date.replace(year=current_date.year-1, month=1, day=1)
        end_date = current_date.replace(year=current_date.year-1, month=12, day=31)
        title_period = f"FY {current_date.year-1}"
    else:  # All Time
        start_date = sales_df['date'].min()
        title_period = f"All Time ({start_date.strftime('%b %Y')} - {current_date.strftime('%b %Y')})"
    
    # Apply date filters
    if report_period in ["Previous Month", "Last Year"]:
        filtered_sales = sales_df[(sales_df['date'] >= start_date) & (sales_df['date'] <= end_date)]
        filtered_purchases = purchases_df[(purchases_df['date'] >= start_date) & (purchases_df['date'] <= end_date)]
        filtered_expenses = expenses_df[(expenses_df['date'] >= start_date) & (expenses_df['date'] <= end_date)]
        filtered_performance = performance_df[(performance_df['date'] >= start_date) & (performance_df['date'] <= end_date)]
    else:
        filtered_sales = sales_df[sales_df['date'] >= start_date]
        filtered_purchases = purchases_df[purchases_df['date'] >= start_date]
        filtered_expenses = expenses_df[expenses_df['date'] >= start_date]
        filtered_performance = performance_df[performance_df['date'] >= start_date]
    
    # Calculate KPIs
    total_revenue = filtered_sales['total_price'].sum()
    total_cost = filtered_purchases['total_cost'].sum()
    total_profit = filtered_sales['profit'].sum()
    total_expenses = filtered_expenses['amount'].sum()
    
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    expense_ratio = (total_expenses / total_revenue * 100) if total_revenue > 0 else 0
    
    # Calculate net profit
    net_profit = total_profit - total_expenses
    net_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    # Get total units sold
    total_units = filtered_sales['quantity'].sum()
    
    # Page title
    st.markdown(f"<h3 style='text-align: center;'>Business Report - {title_period}</h3>", unsafe_allow_html=True)
    
    # Summary KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_metric("Total Revenue", f"${total_revenue:,.2f}"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_metric("Gross Profit", f"${total_profit:,.2f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_metric("Net Profit", f"${net_profit:,.2f}"), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(kpi_metric("Profit Margin", f"{profit_margin:.1f}%"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_metric("Total Expenses", f"${total_expenses:,.2f}"), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_metric("Units Sold", f"{int(total_units):,}"), unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Chart Section
    st.markdown("<h3 style='text-align: center;'>Financial Analysis</h3>", unsafe_allow_html=True)
    
    # Chart 1: Revenue vs Profit Over Time
    # Group by month if the period is longer than 60 days
    if (current_date - start_date).days > 60:
        filtered_sales['month'] = filtered_sales['date'].dt.to_period('M')
        revenue_over_time = filtered_sales.groupby(filtered_sales['month'].astype(str)).agg({
            'total_price': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        x_column = 'month'
        title = 'Monthly Revenue & Profit'
    else:
        revenue_over_time = filtered_sales.groupby(filtered_sales['date'].dt.date).agg({
            'total_price': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        x_column = 'date'
        title = 'Daily Revenue & Profit'
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=revenue_over_time[x_column],
        y=revenue_over_time['total_price'],
        name='Revenue',
        marker_color='#1E3A8A'
    ))
    fig1.add_trace(go.Scatter(
        x=revenue_over_time[x_column],
        y=revenue_over_time['profit'],
        name='Profit',
        marker_color='#28a745',
        mode='lines+markers'
    ))
    
    fig1.update_layout(
        title=title,
        template='plotly_white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE', title='Amount ($)'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Chart 2: Expense Breakdown
    expenses_by_category = filtered_expenses.groupby('category')['amount'].sum().reset_index()
    expenses_by_category = expenses_by_category.sort_values('amount', ascending=False)
    
    fig2 = px.pie(
        expenses_by_category,
        values='amount',
        names='category',
        title='Expense Breakdown',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Reds_r,
        hole=0.4
    )
    fig2.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    # Chart 3: Category Performance
    category_performance = filtered_sales.groupby('category').agg({
        'total_price': 'sum',
        'profit': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    category_performance['margin'] = (category_performance['profit'] / category_performance['total_price'] * 100)
    category_performance = category_performance.sort_values('total_price', ascending=False)
    
    fig3 = px.bar(
        category_performance,
        x='category',
        y=['total_price', 'profit'],
        title='Sales & Profit by Category',
        barmode='group',
        labels={'value': 'Amount ($)', 'category': 'Product Category', 'variable': 'Metric'},
        template='plotly_white',
        color_discrete_map={'total_price': '#1E3A8A', 'profit': '#28a745'}
    )
    
    # Add text annotations
    for i, row in enumerate(category_performance.itertuples()):
        fig3.add_annotation(
            x=row.category,
            y=row.total_price,
            text=f"${row.total_price:,.0f}",
            showarrow=False,
            yshift=10,
            font=dict(color='white', size=10)
        )
    
    fig3.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Chart 4: Monthly Revenue & Expense Comparison
    if report_period in ["Last 6 Months", "Year to Date", "Last Year", "All Time"]:
        # Group sales by month
        filtered_sales['month'] = filtered_sales['date'].dt.to_period('M')
        monthly_revenue = filtered_sales.groupby(filtered_sales['month'].astype(str))['total_price'].sum().reset_index()
        
        # Group expenses by month
        filtered_expenses['month'] = filtered_expenses['date'].dt.to_period('M')
        monthly_expenses = filtered_expenses.groupby(filtered_expenses['month'].astype(str))['amount'].sum().reset_index()
        
        # Merge the data
        financial_data = pd.merge(monthly_revenue, monthly_expenses, on='month', how='outer').fillna(0)
        financial_data.columns = ['month', 'revenue', 'expenses']
        financial_data['profit'] = financial_data['revenue'] - financial_data['expenses']
        
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=financial_data['month'],
            y=financial_data['revenue'],
            name='Revenue',
            marker_color='#1E3A8A'
        ))
        fig4.add_trace(go.Bar(
            x=financial_data['month'],
            y=financial_data['expenses'],
            name='Expenses',
            marker_color='#dc3545'
        ))
        fig4.add_trace(go.Scatter(
            x=financial_data['month'],
            y=financial_data['profit'],
            name='Net Profit',
            line=dict(color='#28a745', width=3),
            mode='lines+markers'
        ))
        
        fig4.update_layout(
            title='Monthly Revenue, Expenses & Profit',
            template='plotly_white',
            plot_bgcolor='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#EEEEEE', title='Amount ($)'),
            margin=dict(l=10, r=10, t=40, b=10),
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            barmode='group'
        )
    else:
        # For shorter periods, show profit margins by product
        product_margins = filtered_sales.groupby(['product_id', 'product_name']).agg({
            'total_price': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        product_margins['margin'] = (product_margins['profit'] / product_margins['total_price'] * 100)
        product_margins = product_margins.sort_values('margin', ascending=False).head(10)
        
        fig4 = px.bar(
            product_margins,
            y='product_name',
            x='margin',
            orientation='h',
            title='Top 10 Products by Profit Margin',
            labels={'product_name': 'Product', 'margin': 'Profit Margin (%)'},
            text=product_margins['margin'].round(1),
            template='plotly_white',
            color='margin',
            color_continuous_scale='Viridis'
        )
        fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig4.update_layout(
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
            yaxis=dict(showgrid=False),
            margin=dict(l=10, r=10, t=40, b=10),
            height=350
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
    
    # Financial Summary Tables
    st.markdown("<h3 style='text-align: center;'>Financial Summary</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Income Statement", "Product Performance", "Export Options"])
    
    with tab1:
        # Simple income statement
        st.markdown("#### Income Statement")
        
        income_data = {
            "Category": ["Revenue", "Cost of Goods Sold", "Gross Profit", "Operating Expenses", "Net Profit"],
            "Amount": [
                total_revenue, 
                total_revenue - total_profit,  # COGS
                total_profit,
                total_expenses,
                net_profit
            ],
            "Percentage": [
                100.0,
                ((total_revenue - total_profit) / total_revenue * 100) if total_revenue > 0 else 0,
                profit_margin,
                expense_ratio,
                net_margin
            ]
        }
        
        income_df = pd.DataFrame(income_data)
        
        # Format the dataframe
        st.dataframe(
            income_df,
            hide_index=True,
            column_config={
                "Category": "Category",
                "Amount": st.column_config.NumberColumn(
                    "Amount",
                    format="$%.2f"
                ),
                "Percentage": st.column_config.NumberColumn(
                    "% of Revenue",
                    format="%.1f%%"
                )
            }
        )
    
    with tab2:
        # Product performance table
        st.markdown("#### Product Performance")
        
        product_performance = filtered_sales.groupby(['product_id', 'product_name', 'category']).agg({
            'quantity': 'sum',
            'total_price': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        product_performance['margin'] = (product_performance['profit'] / product_performance['total_price'] * 100).round(1)
        product_performance = product_performance.sort_values('total_price', ascending=False)
        
        st.dataframe(
            product_performance[['product_name', 'category', 'quantity', 'total_price', 'profit', 'margin']],
            hide_index=True,
            column_config={
                "product_name": "Product",
                "category": "Category",
                "quantity": "Units Sold",
                "total_price": st.column_config.NumberColumn(
                    "Sales Revenue",
                    format="$%.2f"
                ),
                "profit": st.column_config.NumberColumn(
                    "Profit",
                    format="$%.2f"
                ),
                "margin": st.column_config.NumberColumn(
                    "Profit Margin",
                    format="%.1f%%"
                )
            }
        )
    
    with tab3:
        # Export options
        st.markdown("#### Export Report")
        
        export_format = st.selectbox("Select Format", ["Excel (.xlsx)", "CSV", "PDF"])
        
        if st.button("Generate Report"):
            st.success(f"Report for {title_period} has been generated! (Demo - no actual file is created)")
            st.info("In a production environment, this would generate and download the report in the selected format.") 