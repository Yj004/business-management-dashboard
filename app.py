import streamlit as st
import os
from components.auth import authenticate
from components.dashboard import show_dashboard
from components.inventory import show_inventory
from components.purchase import show_purchase
from components.sales import show_sales
from components.performance import show_performance
from components.report import show_report
from utils.styling import apply_custom_styling, display_header, create_sidebar, create_footer
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
generate_initial_data()

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

# Authentication system
if not st.session_state.authenticated:
    authenticate()
else:
    # Display header with user info
    display_header(f"Welcome, {st.session_state.username} ({st.session_state.role})")
    
    # Create sidebar with navigation
    selected_page = create_sidebar()
    
    # Content based on selection
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
    
    # Add a footer
    create_footer()
    
    # Logout button
    if st.sidebar.button("Logout", key="logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun() 