import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))

# Your existing imports start here:
from data_preprocessing import DataLoader, DataCleaning

loader = DataLoader("data/obesity_dataset.xlsx")

data = loader.load_data()

cleaner = DataCleaning(data)

clean_data = cleaner.clean_data()

print("Cleaned Data:")
print(clean_data.head())

print("Shape:", clean_data.shape)