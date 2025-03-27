import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.styling import kpi_metric

def show_performance():
    """Display the performance dashboard with KPIs and charts"""
    
    st.header("Performance Management")
    
    # Load data
    performance_df = pd.read_csv('data/performance.csv')
    sales_df = pd.read_csv('data/sales.csv')
    expenses_df = pd.read_csv('data/expenses.csv')
    
    # Convert date columns to datetime
    performance_df['date'] = pd.to_datetime(performance_df['date'])
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    
    # Filter data for different time periods
    current_date = datetime.now()
    last_month_date = current_date - timedelta(days=30)
    last_2month_date = current_date - timedelta(days=60)
    
    # Get last 30 days performance
    last_30_days_perf = performance_df[performance_df['date'] >= last_month_date]
    prev_30_days_perf = performance_df[(performance_df['date'] >= last_2month_date) & (performance_df['date'] < last_month_date)]
    
    # Sales and expenses for financial KPIs
    last_30_days_sales = sales_df[sales_df['date'] >= last_month_date]
    prev_30_days_sales = sales_df[(sales_df['date'] >= last_2month_date) & (sales_df['date'] < last_month_date)]
    
    last_30_days_expenses = expenses_df[expenses_df['date'] >= last_month_date]
    prev_30_days_expenses = expenses_df[(expenses_df['date'] >= last_2month_date) & (expenses_df['date'] < last_month_date)]
    
    # Calculate KPIs
    # 1. Sales Performance
    total_sales = last_30_days_sales['total_price'].sum()
    prev_sales = prev_30_days_sales['total_price'].sum()
    sales_change_percent = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    
    # 2. Average Customer Satisfaction
    avg_satisfaction = last_30_days_perf['customer_satisfaction'].mean()
    prev_satisfaction = prev_30_days_perf['customer_satisfaction'].mean()
    satisfaction_change = avg_satisfaction - prev_satisfaction
    
    # 3. Profit Margin
    total_profit = last_30_days_sales['profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    prev_profit = prev_30_days_sales['profit'].sum()
    prev_margin = (prev_profit / prev_sales * 100) if prev_sales > 0 else 0
    margin_change = profit_margin - prev_margin
    
    # 4. Average Productivity
    avg_productivity = last_30_days_perf['productivity_score'].mean()
    prev_productivity = prev_30_days_perf['productivity_score'].mean()
    productivity_change = avg_productivity - prev_productivity
    
    # 5. Attendance Rate
    attendance_rate = last_30_days_perf['attendance'].mean() * 100
    prev_attendance = prev_30_days_perf['attendance'].mean() * 100
    attendance_change = attendance_rate - prev_attendance
    
    # 6. Expense to Revenue Ratio
    total_expenses = last_30_days_expenses['amount'].sum()
    expense_ratio = (total_expenses / total_sales * 100) if total_sales > 0 else 0
    prev_expenses = prev_30_days_expenses['amount'].sum()
    prev_expense_ratio = (prev_expenses / prev_sales * 100) if prev_sales > 0 else 0
    ratio_change = expense_ratio - prev_expense_ratio
    
    # KPI Row
    st.markdown("<h3 style='text-align: center;'>Performance Metrics (Last 30 Days)</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(kpi_metric("Sales Performance", f"${total_sales:,.2f}", trend="up" if sales_change_percent > 0 else "down", trend_value=f"{abs(sales_change_percent):.1f}%"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_metric("Customer Satisfaction", f"{avg_satisfaction:.1f}/5.0", trend="up" if satisfaction_change > 0 else "down", trend_value=f"{abs(satisfaction_change):.1f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_metric("Profit Margin", f"{profit_margin:.1f}%", trend="up" if margin_change > 0 else "down", trend_value=f"{abs(margin_change):.1f}%"), unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(kpi_metric("Productivity Score", f"{avg_productivity:.1f}", trend="up" if productivity_change > 0 else "down", trend_value=f"{abs(productivity_change):.1f}"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_metric("Attendance Rate", f"{attendance_rate:.1f}%", trend="up" if attendance_change > 0 else "down", trend_value=f"{abs(attendance_change):.1f}%"), unsafe_allow_html=True)
    with col6:
        st.markdown(kpi_metric("Expense to Revenue", f"{expense_ratio:.1f}%", trend="down" if ratio_change < 0 else "up", trend_value=f"{abs(ratio_change):.1f}%"), unsafe_allow_html=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # Charts
    st.markdown("<h3 style='text-align: center;'>Performance Analysis</h3>", unsafe_allow_html=True)
    
    # Filter for performance data
    time_period = st.selectbox(
        "Select Time Period", 
        ["Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=1
    )
    
    if time_period == "Last 7 Days":
        filter_date = current_date - timedelta(days=7)
    elif time_period == "Last 30 Days":
        filter_date = current_date - timedelta(days=30)
    else:
        filter_date = current_date - timedelta(days=90)
    
    filtered_perf = performance_df[performance_df['date'] >= filter_date]
    
    # Chart 1: Employee Performance Comparison
    employee_perf = filtered_perf.groupby(['employee_name', 'role'])[['sales_value', 'customer_satisfaction', 'productivity_score']].mean().reset_index()
    
    fig1 = px.bar(
        employee_perf,
        x='employee_name',
        y='productivity_score',
        color='role',
        title='Employee Productivity Scores',
        text=employee_perf['productivity_score'].round(1),
        labels={'employee_name': 'Employee', 'productivity_score': 'Productivity Score', 'role': 'Role'},
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 2: Customer Satisfaction Trend
    satisfaction_trend = filtered_perf.groupby(filtered_perf['date'].dt.date)['customer_satisfaction'].mean().reset_index()
    
    fig2 = px.line(
        satisfaction_trend,
        x='date',
        y='customer_satisfaction',
        title='Customer Satisfaction Trend',
        labels={'date': 'Date', 'customer_satisfaction': 'Satisfaction Score'},
        template='plotly_white'
    )
    fig2.update_traces(mode='lines+markers', line=dict(color='#1E3A8A', width=3))
    fig2.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE', range=[3, 5]),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 3: Sales Performance by Employee
    sales_by_employee = filtered_perf.groupby('employee_name')['sales_value'].sum().reset_index()
    sales_by_employee = sales_by_employee.sort_values('sales_value', ascending=False)
    
    fig3 = px.bar(
        sales_by_employee,
        x='employee_name',
        y='sales_value',
        title='Sales Performance by Employee',
        labels={'employee_name': 'Employee', 'sales_value': 'Sales Value ($)'},
        template='plotly_white',
        color='sales_value',
        color_continuous_scale='Blues'
    )
    fig3.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    
    # Chart 4: Attendance Rate by Employee
    attendance_by_employee = filtered_perf.groupby('employee_name')['attendance'].mean().reset_index()
    attendance_by_employee['attendance_rate'] = attendance_by_employee['attendance'] * 100
    attendance_by_employee = attendance_by_employee.sort_values('attendance_rate')
    
    fig4 = px.bar(
        attendance_by_employee,
        x='employee_name',
        y='attendance_rate',
        title='Attendance Rate by Employee',
        labels={'employee_name': 'Employee', 'attendance_rate': 'Attendance Rate (%)'},
        template='plotly_white',
        color='attendance_rate',
        color_continuous_scale='RdYlGn',
        text=attendance_by_employee['attendance_rate'].round(1)
    )
    fig4.update_layout(
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE', range=[60, 100]),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )
    fig4.update_traces(texttemplate='%{text}%', textposition='outside')
    
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
    
    # Employee Performance Details
    st.markdown("<h3 style='text-align: center;'>Employee Performance Details</h3>", unsafe_allow_html=True)
    
    # Allow filtering by role
    role_filter = st.selectbox("Filter by Role", ["All"] + list(filtered_perf['role'].unique()))
    
    if role_filter != "All":
        filtered_perf = filtered_perf[filtered_perf['role'] == role_filter]
    
    # Get employee average metrics
    employee_metrics = filtered_perf.groupby('employee_name').agg({
        'sales_count': 'sum',
        'sales_value': 'sum',
        'customer_satisfaction': 'mean',
        'attendance': 'mean',
        'productivity_score': 'mean'
    }).reset_index()
    
    employee_metrics['attendance_rate'] = (employee_metrics['attendance'] * 100).round(1)
    employee_metrics['customer_satisfaction'] = employee_metrics['customer_satisfaction'].round(1)
    employee_metrics['productivity_score'] = employee_metrics['productivity_score'].round(1)
    
    # Show the dataframe
    st.dataframe(
        employee_metrics[['employee_name', 'sales_count', 'sales_value', 'customer_satisfaction', 'attendance_rate', 'productivity_score']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'employee_name': 'Employee',
            'sales_count': 'Total Sales',
            'sales_value': st.column_config.NumberColumn(
                'Sales Value',
                format="$%.2f"
            ),
            'customer_satisfaction': st.column_config.NumberColumn(
                'Customer Satisfaction',
                format="%.1f"
            ),
            'attendance_rate': st.column_config.NumberColumn(
                'Attendance Rate',
                format="%.1f%%"
            ),
            'productivity_score': st.column_config.NumberColumn(
                'Productivity Score',
                format="%.1f"
            )
        }
    ) 