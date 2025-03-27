import os
from utils.data_generator import regenerate_performance_data

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Regenerate performance data
print("Regenerating performance data...")
regenerate_performance_data()
print("Done! Performance data has been regenerated with the correct structure.") 