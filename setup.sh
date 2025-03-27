#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[theme]
primaryColor = '#1e88e5'
backgroundColor = '#f8f9fa'
secondaryBackgroundColor = '#ffffff'
textColor = '#212529'
font = 'sans serif'

[server]
headless = true
port = $PORT
enableCORS = true
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[global]
developmentMode = false
" > ~/.streamlit/config.toml 