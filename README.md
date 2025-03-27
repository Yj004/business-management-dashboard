# Business Management Dashboard

![Screenshot](assets/dashboard_screenshot.jpg)

## Overview

Business Management Dashboard is a complete business analytics solution built with Streamlit. It provides a comprehensive view of business operations, including sales, inventory, purchases, employee performance, and financial reporting.

## Features

- **Complete Business Analytics**: Track sales, inventory, purchases, performance, and generate reports
- **Interactive Visualizations**: Intuitive charts and graphs powered by Plotly
- **Multi-role Authentication**: Different access levels for Admin, Manager, and Store Manager
- **Responsive Design**: Works on desktop and mobile devices
- **Data Generation**: Includes demo data generator for testing and demonstration

## Modules

- **Dashboard**: Overview of key business metrics and KPIs
- **Inventory**: Track stock levels, reorder points, and inventory value
- **Purchase**: Manage and analyze procurement activities
- **Sales**: Analyze sales trends, top products, and payment methods
- **Performance**: Track employee and business performance metrics
- **Reports**: Generate comprehensive financial and operational reports

## Installation

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Yj004/business-management-dashboard.git
   cd business-management-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

### Deployment to Streamlit Cloud

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## Usage

### Authentication

The dashboard includes a demo authentication system with the following credentials:

| Username | Password  | Role          |
|----------|-----------|---------------|
| admin    | admin123  | Admin         |
| manager  | manager123| Manager       |
| store    | store123  | Store Manager |

### Data

On first run, the application automatically generates sample data for demonstration purposes. In a production environment, you would replace this with your actual business data.

## Customization

The dashboard is designed to be easily customizable:

- **Visual Theme**: Modify the color scheme in `.streamlit/config.toml`
- **Business Logic**: Adapt the business logic in the component files
- **Data Sources**: Connect to your own databases by modifying the data access code

## Project Structure

```
business-management-dashboard/
├── streamlit_app.py        # Main application entry point
├── components/             # Dashboard components
│   ├── auth.py             # Authentication system
│   ├── dashboard.py        # Main dashboard component
│   ├── inventory.py        # Inventory management
│   ├── performance.py      # Performance tracking
│   ├── purchase.py         # Purchase management
│   ├── report.py           # Reporting system
│   └── sales.py            # Sales analysis
├── utils/                  # Utility functions
│   ├── data_generator.py   # Sample data generator
│   ├── styling.py          # UI styling utilities
├── assets/                 # Static assets
├── data/                   # Data files (generated on first run)
├── .streamlit/             # Streamlit configuration
└── requirements.txt        # Dependencies
```

## Recent Fixes

For details about recent fixes and improvements, see [FIXES_APPLIED.md](FIXES_APPLIED.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 