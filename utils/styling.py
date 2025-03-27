import streamlit as st
import plotly.graph_objects as go

def apply_custom_styling():
    """Apply custom styling to the entire application"""
    # Define CSS variables for easy color theming
    st.markdown("""
    <style>
    :root {
        --primary-color: #1e88e5;
        --primary-dark: #1565c0;
        --primary-light: #e3f2fd;
        --secondary-color: #28a745;
        --secondary-dark: #218838;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --success-color: #28a745;
        --background-color: #f8f9fa;
        --card-background: #ffffff;
        --text-color: #212529;
        --text-muted: #6c757d;
        --border-color: #dee2e6;
    }

    /* Main Page Background */
    .main .block-container {
        padding-top: 0.75rem;
        padding-bottom: 0.75rem;
        max-width: 98%;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-size: 0.9rem;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }
    
    h2 {
        font-size: 1.4rem;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #37474f;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 1.25rem;
        color: #455a64;
    }
    
    /* Better Cards and containers */
    .card {
        background-color: var(--card-background);
        border-radius: 6px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        padding: 1rem;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-top: 3px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    
    .card-title {
        color: var(--text-color);
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .card-content {
        color: var(--text-color);
        font-size: 0.85rem;
    }
    
    /* KPI Container */
    .kpi-container {
        background-color: var(--card-background);
        border-radius: 6px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        padding: 0.9rem 1.1rem;
        height: 100%;
        transition: all 0.2s ease;
        border-top: 3px solid var(--primary-color);
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .kpi-container:hover {
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transform: translateY(-3px);
    }
    
    .kpi-title {
        color: var(--text-muted);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        color: var(--text-color);
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
        margin-bottom: 0.4rem;
    }
    
    .trend-up {
        color: var(--success-color);
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.25rem;
        display: flex;
        align-items: center;
    }
    
    .trend-down {
        color: var(--danger-color);
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.25rem;
        display: flex;
        align-items: center;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: var(--card-background);
    }
    
    .sidebar .sidebar-content {
        background-color: var(--card-background);
    }
    
    /* Header & Banners */
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: var(--card-background);
        border-radius: 6px;
        padding: 0.8rem 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        border-left: none;
        border-top: 3px solid var(--primary-color);
    }
    
    .app-title {
        color: var(--primary-color);
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        color: var(--text-color);
        font-weight: 500;
        background-color: var(--primary-light);
        padding: 0.3rem 0.8rem;
        border-radius: 18px;
        font-size: 0.85rem;
    }
    
    .user-icon {
        margin-right: 0.4rem;
        color: var(--primary-color);
    }
    
    .info-banner {
        background-color: #e3f2fd;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--primary-color);
        color: var(--text-color);
        font-size: 0.85rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .warning-banner {
        background-color: #fff3cd;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--warning-color);
        color: var(--text-color);
        font-size: 0.85rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .error-banner {
        background-color: #f8d7da;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--danger-color);
        color: var(--text-color);
        font-size: 0.85rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    /* Button styles */
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 4px;
        padding: 0.4rem 0.9rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.75rem;
    }
    
    .stButton button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        transform: translateY(-1px);
    }
    
    .secondary-button button {
        background-color: var(--secondary-color);
    }
    
    .secondary-button button:hover {
        background-color: var(--secondary-dark);
    }
    
    .warning-button button {
        background-color: var(--warning-color);
    }
    
    .danger-button button {
        background-color: var(--danger-color);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f8f9fa;
        border-radius: 6px 6px 0 0;
        padding: 0 8px;
        border: 1px solid var(--border-color);
        border-bottom: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 0.6rem 1rem;
        font-weight: 500;
        color: var(--text-muted);
        transition: all 0.2s ease;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom: 2px solid var(--primary-color);
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        border-radius: 0 0 6px 6px;
        padding: 1rem;
        border: 1px solid var(--border-color);
        border-top: none;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }
    
    /* Table styles */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        overflow: hidden;
        margin: 0.75rem 0;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        font-size: 0.8rem;
    }
    
    .dataframe thead th {
        background-color: #f8f9fa;
        padding: 0.6rem 0.75rem;
        text-align: left;
        font-weight: 600;
        color: var(--text-color);
        border-bottom: 1px solid var(--border-color);
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid var(--border-color);
        transition: background-color 0.2s ease;
    }
    
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #f8f9fa;
    }
    
    .dataframe tbody tr:hover {
        background-color: #e3f2fd;
    }
    
    .dataframe tbody td {
        padding: 0.6rem 0.75rem;
        color: var(--text-color);
    }
    
    /* Radio buttons and checkboxes */
    .stRadio > div {
        background-color: var(--card-background);
        border-radius: 6px;
        padding: 0.75rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }
    
    /* Text inputs, selects, and number inputs */
    .stTextInput > div > div, .stSelectbox > div, .stNumberInput > div {
        background-color: var(--card-background);
        border-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    
    .stTextInput > label, .stSelectbox > label, .stNumberInput > label {
        background-color: transparent;
        color: var(--text-color);
        font-weight: 500;
        font-size: 0.85rem;
    }
    
    /* Footer */
    .footer {
        background-color: var(--card-background);
        padding: 0.8rem 1.2rem;
        margin-top: 2rem;
        border-radius: 6px;
        text-align: center;
        color: var(--text-muted);
        font-size: 0.75rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        border-top: 3px solid var(--primary-color);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 8px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    
    /* Stat Row Component */
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--border-color);
        align-items: center;
        font-size: 0.85rem;
    }
    
    .stat-row:last-child {
        border-bottom: none;
    }
    
    .stat-label {
        color: var(--text-color);
        font-weight: 500;
        display: flex;
        align-items: center;
    }
    
    .stat-value {
        color: var(--primary-color);
        font-weight: 600;
    }
    
    .stat-icon {
        margin-right: 0.4rem;
    }

    /* Plot styling */
    .js-plotly-plot {
        border-radius: 6px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        padding: 0.4rem;
        background: white;
        margin-bottom: 1rem;
    }

    /* Login page styling */
    .login-container {
        background-color: white;
        border-radius: 6px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        padding: 1.5rem;
        border-top: 3px solid var(--primary-color);
    }

    .login-header {
        color: var(--primary-color);
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    /* Navbar styling */
    .nav-link {
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        border-radius: 6px;
        color: var(--text-color);
        text-decoration: none;
        transition: all 0.2s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        font-size: 0.85rem;
    }

    .nav-link:hover {
        background-color: var(--primary-light);
        color: var(--primary-color);
    }

    .nav-link.active {
        background-color: var(--primary-color);
        color: white;
    }

    .nav-icon {
        margin-right: 0.6rem;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def kpi_metric(title, value, trend="neutral", trend_value="", prefix="", suffix=""):
    """Generate HTML for a KPI metric"""
    trend_class = "trend-up" if trend == "up" else "trend-down" if trend == "down" else ""
    trend_icon = "▲" if trend == "up" else "▼" if trend == "down" else ""
    
    # Combine prefix, value and suffix
    display_value = f"{prefix}{value}{suffix}"
    
    return f"""
    <div class="kpi-container">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{display_value}</div>
        <div class="{trend_class}">{trend_icon} {trend_value}</div>
    </div>
    """

def card(title, content):
    """Generate HTML for a card component"""
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-content">{content}</div>
    </div>
    """

def info_banner(message):
    """Generate HTML for an info banner"""
    return st.markdown(f"""
    <div class="info-banner">
        <strong>Info:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def warning_banner(message):
    """Generate HTML for a warning banner"""
    return st.markdown(f"""
    <div class="warning-banner">
        <strong>Warning:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def error_banner(message):
    """Generate HTML for an error banner"""
    return st.markdown(f"""
    <div class="error-banner">
        <strong>Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def stat_row(label, value, icon="", value_color=""):
    """Generate HTML for a stat row with a label and value"""
    icon_html = f'<span class="stat-icon">{icon}</span>' if icon else ''
    value_style = f'style="color: {value_color};"' if value_color else ''
    
    return f"""
    <div class="stat-row">
        <div class="stat-label">{icon_html}{label}</div>
        <div class="stat-value" {value_style}>{value}</div>
    </div>
    """

def display_header(title_text):
    """Display the application header with user info"""
    st.markdown(f"""
    <div class="app-header">
        <h1 class="app-title">Business Management Dashboard</h1>
        <div class="user-info">
            <span class="user-icon">👤</span> {title_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create the navigation sidebar and return the selected page"""
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="color: var(--primary-color); margin-bottom: 15px; font-size: 1.2rem;">Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options
    pages = {
        "Dashboard": "📊",
        "Inventory": "📦",
        "Purchase": "🛒",
        "Sales": "💰",
        "Performance": "📈",
        "Report": "📝"
    }
    
    # Create navigation buttons with better styling
    selected_page = None
    
    for page, icon in pages.items():
        if st.sidebar.button(f"{icon} {page}", key=f"nav_{page}", 
                            help=f"Navigate to {page}"):
            selected_page = page
    
    # If nothing selected, default to Dashboard
    if selected_page is None:
        selected_page = "Dashboard"
    
    # Show user role info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 6px; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); font-size: 0.85rem;">
        <p style="margin-bottom: 5px; font-weight: 600;">User Information</p>
        <strong>Role:</strong> {st.session_state.role}<br>
        <strong>Access:</strong> Full
    </div>
    """, unsafe_allow_html=True)
    
    return selected_page

def create_footer():
    """Create a footer for the application"""
    st.markdown("""
    <div class="footer">
        <p>Business Management Dashboard © 2023 | All data is for demonstration purposes only</p>
        <p>Version 1.0.0 | Last updated: November 2023</p>
    </div>
    """, unsafe_allow_html=True)

def create_plotly_template():
    """Create a consistent Plotly template for all charts"""
    template = go.layout.Template()
    template.layout = go.Layout(
        font=dict(family="'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif", size=11, color="#212529"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        colorway=["#1e88e5", "#28a745", "#9c27b0", "#ffc107", "#00bcd4", "#dc3545"],
        xaxis=dict(
            showgrid=True,
            gridcolor="#f0f0f0",
            zeroline=False,
            showline=True,
            linecolor="#dee2e6"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f0f0f0",
            zeroline=False,
            showline=True,
            linecolor="#dee2e6"
        ),
        margin=dict(l=30, r=10, t=30, b=30),
        hovermode="closest",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    return template 