import streamlit as st
import os
import pandas as pd
from components.auth import authenticate
from components.dashboard import show_dashboard
from components.inventory import show_inventory
from components.purchase import show_purchase
from components.sales import show_sales
from components.performance import show_performance
from components.report import show_report
from utils.styling import apply_custom_styling, display_header, create_sidebar, create_footer, warning_banner
from utils.data_generator import generate_initial_data

# Set up page config with improved layout and title
st.set_page_config(
    page_title="Business Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Check if directories exist or create them
if not os.path.exists("data"):
    os.makedirs("data")
    
if not os.path.exists("assets"):
    os.makedirs("assets")

# Generate initial data if needed
try:
    generate_initial_data()
except Exception as e:
    st.error(f"Error generating initial data: {str(e)}")
    st.info("Please try refreshing the page. If the error persists, contact support.")

# Function to check if required data files exist
def check_data_files():
    required_files = [
        'data/products.csv',
        'data/inventory.csv',
        'data/sales.csv',
        'data/purchases.csv',
        'data/expenses.csv',
        'data/employees.csv',
        'data/performance.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

# Authentication system
if not st.session_state.authenticated:
    # Check for missing data files before authentication
    missing_files = check_data_files()
    if missing_files:
        st.error("Some required data files are missing. Please reload the page to generate the data.")
        st.write("Missing files:", ", ".join(missing_files))
    else:
        authenticate()
else:
    # Check for missing data files after authentication
    missing_files = check_data_files()
    if missing_files:
        st.error("Some required data files are missing. Please reload the page to generate the data.")
        st.write("Missing files:", ", ".join(missing_files))
    else:
        try:
            # Display header with user info
            display_header(f"Welcome, {st.session_state.username} ({st.session_state.role})")
            
            # Create sidebar with navigation
            selected_page = create_sidebar()
            
            # Content based on selection with error handling
            try:
                if selected_page == "Dashboard":
                    show_dashboard()
                elif selected_page == "Inventory":
                    show_inventory()
                elif selected_page == "Purchase":
                    show_purchase()
                elif selected_page == "Sales":
                    show_sales()
                elif selected_page == "Performance":
                    show_performance()
                elif selected_page == "Report":
                    show_report()
            except Exception as e:
                st.error(f"Error loading {selected_page} component: {str(e)}")
                st.info("This may be due to missing or corrupted data. Try refreshing the page.")
            
            # Add a footer
            create_footer()
            
            # Logout button
            if st.sidebar.button("Logout", key="logout"):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.role = ""
                st.rerun()
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.info("Please try refreshing the page. If the error persists, contact support.") 