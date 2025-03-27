import os
import subprocess
import sys
import webbrowser
from time import sleep

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        import matplotlib
        from PIL import Image
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install all required dependencies using:")
        print("pip install -r requirements.txt")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("╔════════════════════════════════════════════════╗")
    print("║       Business Management Dashboard             ║")
    print("╚════════════════════════════════════════════════╝")
    print("\nChecking dependencies...")
    
    if not check_dependencies():
        print("\nWould you like to install the required dependencies now? (y/n)")
        choice = input().lower()
        if choice == 'y':
            print("Installing dependencies...")
            subprocess.call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print("Please install dependencies manually and try again.")
            return
    
    print("\nGenerating initial data...")
    
    # Make sure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Make sure the assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    print("\nStarting the dashboard...")
    print("\nThe dashboard will open in your default web browser shortly...")
    print("Press Ctrl+C to stop the server when you're done.")
    
    # Open the browser after a short delay to give Streamlit time to start
    sleep(2)
    webbrowser.open('http://localhost:8501')
    
    # Start the Streamlit server
    subprocess.call([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    launch_dashboard() 