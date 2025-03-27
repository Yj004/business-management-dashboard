import streamlit as st
import os
import hashlib
from PIL import Image
from utils.image_handler import ensure_images_exist
from utils.styling import warning_banner, info_banner

def authenticate():
    """Handle user authentication and return authentication status"""
    # Ensure required images exist
    ensure_images_exist()
    
    # Mock user data for demonstration
    users = {
        "admin": {
            "password": "admin123",
            "role": "Admin"
        },
        "manager": {
            "password": "manager123",
            "role": "Manager"
        },
        "store": {
            "password": "store123",
            "role": "Store Manager"
        }
    }
    
    # Check if assets directory exists and create if not
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Apply custom padding to the main container
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login page layout with two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #1e88e5; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">Business Management Dashboard</h1>
            <p style="color: #6c757d; font-size: 1.1rem;">Sign in to access your dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stylish login container
        st.markdown("""
        <div style="background-color: white; padding: 2.5rem; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-top: 4px solid #1e88e5; margin-bottom: 1.5rem;">
            <h3 style="color: #212529; text-align: center; margin-bottom: 1.5rem; font-weight: 600;">Login to Your Account</h3>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Role selection dropdown with better styling
            role_options = ["Admin", "Manager", "Store Manager"]
            role = st.selectbox("Select Role", role_options)
            
            # Info about available accounts
            st.markdown("""
            <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0; font-size: 0.9rem;">
                <p style="margin-bottom: 0.5rem; font-weight: 600;">Available Demo Accounts:</p>
                <ul style="margin-bottom: 0; padding-left: 1.5rem;">
                    <li><strong>Admin:</strong> username: admin, password: admin123</li>
                    <li><strong>Manager:</strong> username: manager, password: manager123</li>
                    <li><strong>Store Manager:</strong> username: store, password: store123</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Login button with styling
            login_button = st.form_submit_button("Sign In")
            
        # Close the login container div
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Display logo/welcome image
        if os.path.exists("assets/login_image.png"):
            image = Image.open("assets/login_image.png")
            st.image(image, use_column_width=True)
        
        # Display welcome information
        st.markdown("""
        <div style="background-color: white; padding: 2rem; border-radius: 8px; margin-top: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-top: 4px solid #28a745;">
            <h4 style="color: #212529; margin-bottom: 1rem; font-weight: 600;">Welcome to the Business Dashboard</h4>
            
            <p style="color: #6c757d; margin-bottom: 1.5rem;">A complete solution to manage and monitor all aspects of your business operations.</p>
            
            <div style="margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background-color: #e3f2fd; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; color: #1e88e5; font-size: 1.25rem;">📊</div>
                    <div>
                        <p style="margin: 0; font-weight: 600; color: #212529;">Data Analytics</p>
                        <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Real-time metrics and visualizations</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background-color: #e8f5e9; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; color: #28a745; font-size: 1.25rem;">📦</div>
                    <div>
                        <p style="margin: 0; font-weight: 600; color: #212529;">Inventory Management</p>
                        <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Track stock levels and automate ordering</p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background-color: #fff8e1; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; color: #ffc107; font-size: 1.25rem;">💰</div>
                    <div>
                        <p style="margin: 0; font-weight: 600; color: #212529;">Sales & Performance</p>
                        <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">Comprehensive sales tracking and reporting</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Login validation
    if login_button:
        if not username or not password:
            warning_banner("Please enter both username and password.")
            return
            
        if username in users and users[username]["password"] == password and users[username]["role"] == role:
            # Successful login
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.rerun()
        else:
            # Failed login
            warning_banner("Invalid username, password, or role combination. Please try again.")
            
    # Default return (not authenticated)
    return 