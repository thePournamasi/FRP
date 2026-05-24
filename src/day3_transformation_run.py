from data_preprocessing import DataLoader, DataCleaning
from feature_engineering import FeatureEngineering

# correct file name
loader = DataLoader("data/obesity_dataset.xlsx")

data = loader.load_data()

# Day 2 cleaning
cleaner = DataCleaning(data)
clean_data = cleaner.clean_data()
print(clean_data.columns)

print("After Cleaning:", clean_data.shape)

# Day 3 transformation
engineer = FeatureEngineering(clean_data)

X, y = engineer.transform()

print("\nX sample:")
print(X.head())

print("\ny sample:")
print(y.head())


print("\nShape of X:", X.shape)
print("Shape of y:", y.shape)
