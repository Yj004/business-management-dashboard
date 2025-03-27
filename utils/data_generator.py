import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta
import json

def generate_initial_data():
    """Generate initial data for the dashboard if it doesn't exist"""
    
    # Check if data files already exist
    if os.path.exists('data/products.csv') and \
       os.path.exists('data/inventory.csv') and \
       os.path.exists('data/sales.csv') and \
       os.path.exists('data/purchases.csv') and \
       os.path.exists('data/expenses.csv') and \
       os.path.exists('data/employees.csv') and \
       os.path.exists('data/performance.csv'):
        return
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate product data
    products = generate_product_data()
    
    # Generate inventory data
    generate_inventory_data(products)
    
    # Generate sales data
    generate_sales_data(products)
    
    # Generate purchase orders data
    generate_purchase_data(products)
    
    # Generate expense data
    generate_expense_data()
    
    # Generate employee performance data
    generate_employee_data()
    
    print("Initial data generated successfully!")

def generate_product_data():
    """Generate and save product data"""
    
    # Products data
    products = [
        {"id": 1, "name": "Product A", "category": "Electronics", "cost": 120, "price": 200},
        {"id": 2, "name": "Product B", "category": "Electronics", "cost": 80, "price": 150},
        {"id": 3, "name": "Product C", "category": "Clothing", "cost": 30, "price": 60},
        {"id": 4, "name": "Product D", "category": "Clothing", "cost": 25, "price": 45},
        {"id": 5, "name": "Product E", "category": "Home", "cost": 50, "price": 90},
        {"id": 6, "name": "Product F", "category": "Home", "cost": 70, "price": 120},
        {"id": 7, "name": "Product G", "category": "Food", "cost": 10, "price": 18},
        {"id": 8, "name": "Product H", "category": "Food", "cost": 5, "price": 10},
    ]
    
    # Save products data
    pd.DataFrame(products).to_csv('data/products.csv', index=False)
    
    return products

def generate_inventory_data(products):
    """Generate and save inventory data"""
    
    # Generate dates for last 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date)
    
    # Generate inventory data
    inventory = []
    for product in products:
        inventory.append({
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "current_stock": random.randint(10, 100),
            "reorder_level": random.randint(5, 20),
            "last_restocked": dates[random.randint(0, len(dates)-1)].strftime('%Y-%m-%d'),
            "unit_cost": product["cost"],
            "total_value": product["cost"] * random.randint(10, 100)
        })
    
    # Save inventory data
    pd.DataFrame(inventory).to_csv('data/inventory.csv', index=False)

def generate_sales_data(products):
    """Generate and save sales data"""
    
    # Generate dates for last 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date)
    
    # Generate sales data
    sales = []
    for date in dates:
        daily_sales = random.randint(5, 30)  # Number of sales per day
        for _ in range(daily_sales):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            sales.append({
                "date": date.strftime('%Y-%m-%d'),
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": product["price"],
                "total_price": product["price"] * quantity,
                "profit": (product["price"] - product["cost"]) * quantity,
                "customer_id": random.randint(1, 50),
                "payment_method": random.choice(["Cash", "Credit Card", "Digital Wallet"])
            })
    
    # Save sales data
    pd.DataFrame(sales).to_csv('data/sales.csv', index=False)

def generate_purchase_data(products):
    """Generate and save purchase (procurement) data"""
    
    # Generate dates for last 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date)
    
    # Generate purchase (procurement) data
    purchases = []
    for i in range(100):
        date = dates[random.randint(0, len(dates)-1)]
        product = random.choice(products)
        quantity = random.randint(10, 100)
        purchases.append({
            "date": date.strftime('%Y-%m-%d'),
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "quantity": quantity,
            "unit_cost": product["cost"],
            "total_cost": product["cost"] * quantity,
            "supplier_id": random.randint(1, 10),
            "status": random.choice(["Delivered", "Pending", "Ordered"])
        })
    
    # Save purchase data
    pd.DataFrame(purchases).to_csv('data/purchases.csv', index=False)

def generate_expense_data():
    """Generate and save expenses data"""
    
    # Generate dates for last 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date)
    
    # Generate expenses data
    expense_categories = ["Rent", "Utilities", "Salaries", "Marketing", "Supplies", "Maintenance", "Insurance", "Miscellaneous"]
    expenses = []
    
    for date in pd.date_range(start=dates[0], end=dates[-1], freq='M'):
        for category in expense_categories:
            if category == "Rent":
                amount = random.randint(4000, 5000)
            elif category == "Utilities":
                amount = random.randint(1000, 1500)
            elif category == "Salaries":
                amount = random.randint(15000, 20000)
            elif category == "Marketing":
                amount = random.randint(2000, 3000)
            else:
                amount = random.randint(500, 2000)
                
            expenses.append({
                "date": date.strftime('%Y-%m-%d'),
                "category": category,
                "amount": amount,
                "description": f"{category} expenses for {date.strftime('%B %Y')}"
            })
    
    # Save expenses data
    pd.DataFrame(expenses).to_csv('data/expenses.csv', index=False)

def generate_employee_data():
    """Generate employee performance data"""
    
    # Employee names
    first_names = ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava', 'Benjamin', 'Isabella',
                   'Ethan', 'Mia', 'Alexander', 'Charlotte', 'Daniel', 'Amelia', 'Matthew', 'Harper', 'David', 'Evelyn']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                  'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson']
    
    # Roles and departments
    roles = ['Sales Associate', 'Sales Manager', 'Marketing Specialist', 'Customer Support', 'Inventory Specialist', 
             'Office Manager', 'HR Specialist', 'Account Manager', 'Warehouse Manager', 'Administrative Assistant']
    
    departments = ['Sales', 'Marketing', 'Customer Service', 'Warehouse', 'Administration']
    
    # Generate employees
    employees = []
    for i in range(1, 21):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        department = random.choice(departments)
        role = random.choice(roles)
        
        join_date = (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime('%Y-%m-%d')
        
        employees.append({
            'employee_id': i,
            'name': name,
            'department': department,
            'position': role,
            'join_date': join_date
        })
    
    employees_df = pd.DataFrame(employees)
    employees_df.to_csv('data/employees.csv', index=False)
    
    # Generate daily performance data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Last 6 months
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create daily performance records
    performance_data = []
    
    for date in dates:
        # Not every employee has a record every day (weekends, days off, etc.)
        active_employees = random.sample(employees, random.randint(10, 20))
        
        for employee in active_employees:
            # Generate performance metrics
            sales_count = random.randint(0, 20) if employee['department'] == 'Sales' else random.randint(0, 5)
            sales_value = sales_count * random.randint(100, 1000)
            customer_satisfaction = round(random.uniform(3.0, 5.0), 1)  # Scale of 1-5
            attendance = 1.0  # Present
            productivity_score = round(random.uniform(60, 100), 1)  # Scale of 0-100
            
            performance_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'employee_id': employee['employee_id'],
                'employee_name': employee['name'],
                'role': employee['position'],
                'department': employee['department'],
                'sales_count': sales_count,
                'sales_value': sales_value,
                'customer_satisfaction': customer_satisfaction,
                'attendance': attendance,
                'productivity_score': productivity_score
            })
    
    # Add some absent days (attendance = 0)
    for _ in range(len(employees) * 5):  # About 5 absences per employee on average
        random_date = random.choice(dates)
        random_employee = random.choice(employees)
        
        # Check if this employee already has a record for this date
        existing_records = [item for item in performance_data 
                           if item['date'] == random_date.strftime('%Y-%m-%d') 
                           and item['employee_id'] == random_employee['employee_id']]
        
        if not existing_records:
            performance_data.append({
                'date': random_date.strftime('%Y-%m-%d'),
                'employee_id': random_employee['employee_id'],
                'employee_name': random_employee['name'],
                'role': random_employee['position'],
                'department': random_employee['department'],
                'sales_count': 0,
                'sales_value': 0,
                'customer_satisfaction': 0,
                'attendance': 0.0,  # Absent
                'productivity_score': 0
            })
    
    # Save performance data
    performance_df = pd.DataFrame(performance_data)
    performance_df.to_csv('data/performance.csv', index=False) 

# New function to regenerate performance data only
def regenerate_performance_data():
    """Regenerate only the performance data with the correct structure"""
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Load existing employees or generate if not exists
    if os.path.exists('data/employees.csv'):
        employees_df = pd.read_csv('data/employees.csv')
        employees = employees_df.to_dict('records')
    else:
        # Generate and save employee data if not exists
        employees = []
        for i in range(1, 21):
            first_name = random.choice([
                'John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 
                'James', 'Ava', 'Benjamin', 'Isabella'
            ])
            last_name = random.choice([
                'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 
                'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor'
            ])
            name = f"{first_name} {last_name}"
            
            department = random.choice([
                'Sales', 'Marketing', 'Customer Service', 'Warehouse', 'Administration'
            ])
            role = random.choice([
                'Sales Associate', 'Sales Manager', 'Marketing Specialist', 
                'Customer Support', 'Inventory Specialist', 'Office Manager'
            ])
            
            join_date = (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime('%Y-%m-%d')
            
            employees.append({
                'employee_id': i,
                'name': name,
                'department': department,
                'position': role,
                'join_date': join_date
            })
        
        # Save employees data
        pd.DataFrame(employees).to_csv('data/employees.csv', index=False)
    
    # Generate daily performance data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Last 6 months
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create daily performance records
    performance_data = []
    
    for date in dates:
        # Not every employee has a record every day (weekends, days off, etc.)
        active_employees = random.sample(employees, min(len(employees), random.randint(10, 20)))
        
        for employee in active_employees:
            # Handle different column names between potential DataFrames and dictionaries
            employee_id = employee.get('employee_id', employee.get('id', 0))
            employee_name = employee.get('name', '')
            role = employee.get('position', employee.get('role', ''))
            department = employee.get('department', '')
            
            # Generate performance metrics
            sales_count = random.randint(0, 20) if 'Sales' in department else random.randint(0, 5)
            sales_value = sales_count * random.randint(100, 1000)
            customer_satisfaction = round(random.uniform(3.0, 5.0), 1)  # Scale of 1-5
            attendance = 1.0  # Present
            productivity_score = round(random.uniform(60, 100), 1)  # Scale of 0-100
            
            performance_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'employee_id': employee_id,
                'employee_name': employee_name,
                'role': role,
                'department': department,
                'sales_count': sales_count,
                'sales_value': sales_value,
                'customer_satisfaction': customer_satisfaction,
                'attendance': attendance,
                'productivity_score': productivity_score
            })
    
    # Add some absent days (attendance = 0)
    for _ in range(len(employees) * 5):  # About 5 absences per employee on average
        random_date = random.choice(dates)
        random_employee = random.choice(employees)
        
        # Handle different column names
        employee_id = random_employee.get('employee_id', random_employee.get('id', 0))
        employee_name = random_employee.get('name', '')
        role = random_employee.get('position', random_employee.get('role', ''))
        department = random_employee.get('department', '')
        
        # Check if this employee already has a record for this date
        existing_records = [item for item in performance_data 
                           if item['date'] == random_date.strftime('%Y-%m-%d') 
                           and item['employee_id'] == employee_id]
        
        if not existing_records:
            performance_data.append({
                'date': random_date.strftime('%Y-%m-%d'),
                'employee_id': employee_id,
                'employee_name': employee_name,
                'role': role,
                'department': department,
                'sales_count': 0,
                'sales_value': 0,
                'customer_satisfaction': 0,
                'attendance': 0.0,  # Absent
                'productivity_score': 0
            })
    
    # Save performance data
    performance_df = pd.DataFrame(performance_data)
    performance_df.to_csv('data/performance.csv', index=False)
    print(f"Generated {len(performance_data)} performance records for {len(employees)} employees") 