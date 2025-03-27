# Streamlit Cloud Deployment Guide

This document provides a step-by-step guide to deploy the Business Management Dashboard on Streamlit Cloud.

## Prerequisites

Before deploying to Streamlit Cloud, make sure you have:

1. A GitHub account
2. The complete dashboard codebase
3. A Streamlit Cloud account (free tier available at [https://streamlit.io/cloud](https://streamlit.io/cloud))

## Deployment Steps

### 1. Prepare your GitHub Repository

1. Create a new GitHub repository or use an existing one
2. Upload all the project files, making sure to include:
   - `streamlit_app.py` (main entry point)
   - `/components` directory with all component files 
   - `/utils` directory with all utility files
   - `/assets` directory (even if empty)
   - `requirements.txt` with all dependencies
   - `.streamlit/config.toml` for theme configuration
   - `.gitignore` file

### 2. Deploy on Streamlit Cloud

1. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click the "New app" button
3. Connect your GitHub account if not already connected
4. Select the repository containing your dashboard
5. Configure the app:
   - Main file path: `streamlit_app.py`
   - Branch: `main` (or your preferred branch)
   - App URL: Choose a custom subdomain if desired
6. Click "Deploy"

### 3. Verify Deployment

After deployment completes:

1. Check that the app loads correctly
2. Test the login with different user roles:
   - Admin: `admin` / `admin123`
   - Manager: `manager` / `manager123`
   - Store Manager: `store` / `store123`
3. Verify that all components load properly
4. Check if the data is generated correctly

## Handling Common Issues

### Data Generation Issues

If you experience data generation errors:

1. **Issue**: Missing CSV files or data not showing up
   - **Solution**: Ensure the `/data` directory exists. The app will attempt to create it and generate data automatically.
   - **Advanced Solution**: You can manually set up initial data by deploying a small dataset in the repository.

2. **Issue**: Performance or Report data errors
   - **Solution**: These components expect specific data fields. Make sure the data generator has been updated with the latest schema.

### Authentication Issues

1. **Issue**: Login not working
   - **Solution**: Verify the authentication code uses `st.rerun()` rather than the deprecated `st.experimental_rerun()`.

2. **Issue**: Session state not persisting
   - **Solution**: Streamlit Cloud handles session state differently than local development. Use `st.session_state` consistently throughout the app.

### Styling Issues

1. **Issue**: Theme not applied
   - **Solution**: Verify the `.streamlit/config.toml` file is correctly formatted and present in the repository.

2. **Issue**: UI elements misaligned
   - **Solution**: Streamlit Cloud may render elements slightly differently. Test with different screen sizes.

### Resource Limitations

Streamlit Cloud Free Tier has some limitations:

1. App will spin down after inactivity (typically 7 days)
2. Shared CPU/Memory resources might affect performance
3. Public URL means anyone can access your app

Upgrading to a paid plan can eliminate these limitations.

## Customizing Your Deployment

### Custom Domain

1. Go to your app settings in Streamlit Cloud
2. Under "General" tab, locate the "Custom domain" section
3. Follow the instructions to set up your domain

### Environment Variables

For sensitive information or configuration:

1. Go to your app settings in Streamlit Cloud
2. Under "Secrets" tab, add key-value pairs
3. Access in your app using `st.secrets["your_key"]`

### GitHub Integration

When you push changes to your GitHub repository:

1. Streamlit Cloud automatically rebuilds your app
2. No manual redeployment needed
3. Track build status in the Streamlit Cloud dashboard

## Monitoring and Maintenance

### Viewing Logs

1. Go to your app settings in Streamlit Cloud
2. Under "Logs" tab, view app logs
3. Useful for debugging deployment issues

### Managing App Resources

1. Go to your app settings in Streamlit Cloud
2. Under "Resources" tab, manage app resources (paid plans)
3. Restart your app if needed

## Support Resources

If you encounter issues:

1. Streamlit Documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)
2. Streamlit Community Forum: [https://discuss.streamlit.io/](https://discuss.streamlit.io/)
3. Streamlit Cloud Specific FAQs: [https://docs.streamlit.io/streamlit-cloud](https://docs.streamlit.io/streamlit-cloud)

## Conclusion

With these steps, your Business Management Dashboard should be successfully deployed to Streamlit Cloud. The dashboard provides a complete business analytics solution with multi-role authentication, six key functional sections, and professional data visualization. 