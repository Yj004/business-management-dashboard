# Business Management Dashboard - Deployment Guide

This guide provides instructions on how to deploy the Business Management Dashboard to Streamlit Cloud.

## Overview

The Business Management Dashboard is a complete business analytics solution with:

- Multi-role authentication (Admin, Manager, Store Manager)
- Six key sections (Dashboard, Inventory, Purchase, Sales, Performance, Reports)
- Dynamic data visualization with interactive charts
- Professional styling and modern UI

## Deployment to Streamlit Cloud

Follow these steps to deploy the dashboard to Streamlit Cloud:

### 1. Create a GitHub Repository

1. Create a new GitHub repository
2. Upload all the project files to this repository
3. Make sure your repository includes:
   - `streamlit_app.py` (main entry point)
   - `/components` directory
   - `/utils` directory
   - `/assets` directory
   - `requirements.txt`
   - `.gitignore`

### 2. Connect to Streamlit Cloud

1. Sign up for or log in to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click on "New app"
3. Connect your GitHub account if not already connected
4. Select the repository containing the dashboard
5. Set the main file path to `streamlit_app.py`
6. Click "Deploy"

### 3. Advanced Settings (Optional)

You can customize your deployment with:

- **Custom domain**: In the app settings, you can set up a custom subdomain
- **Secrets management**: If using external services, manage secrets in the Streamlit Cloud dashboard
- **Resource allocation**: Adjust based on your application's needs

## Authentication

The dashboard includes a demo authentication system with the following credentials:

| Username | Password  | Role           |
|----------|-----------|----------------|
| admin    | admin123  | Admin          |
| manager  | manager123| Manager        |
| store    | store123  | Store Manager  |

## Data Generation

The application automatically generates demo data on first run. In a production environment, you would:

1. Replace the data generation with connections to your actual databases
2. Update the data access logic in the components
3. Consider implementing proper authentication with JWT or OAuth

## Troubleshooting

If you encounter issues during deployment:

1. Check the logs in the Streamlit Cloud dashboard
2. Verify all dependencies are correctly specified in `requirements.txt`
3. Ensure the `streamlit_app.py` file is at the root of your repository
4. Confirm all necessary directories exist and are correctly referenced

### Common Pandas Warnings and Fixes

The application has been updated to address several common pandas warnings:

1. **Pandas Frequency Parameter Confusion**: For time-based operations, we use:
   - `to_period('M')` for converting dates to periods (Month)
   - `resample('ME')` for resampling operations (Month End)
   - This specific distinction is important as pandas uses different frequency aliases for different operations

2. **Inplace Method Warning**: We've updated pandas operations to avoid using `inplace=True` which is being deprecated, following the recommended pattern of `df[col] = df[col].method()` instead.

3. **Experimental API Warning**: All instances of `st.experimental_rerun()` have been updated to `st.rerun()`, which is the current stable API.

4. **Data Generation**: Fixed issues where data columns were missing or incorrectly formatted, particularly for performance and report data.

If you see any more pandas warnings, you can update them following similar patterns.

## Maintenance and Updates

After deployment:

1. Any push to the connected branch will trigger a redeployment
2. You can manage app settings, view logs, and monitor performance in the Streamlit Cloud dashboard
3. Use the "Reboot app" option in the dashboard if you need to force a restart

## Support

If you need assistance with deployment or customization, contact the development team for support. 