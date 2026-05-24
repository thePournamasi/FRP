import os
from data_preprocessing import DataLoader
from sklearn.model_selection import train_test_split

# Path of dataset
data_path = "data/obesity_dataset.xlsx"

# Load the data
loader = DataLoader(data_path)
data = loader.load_data()

print("--- Initial Data Preview ---")
print(data.head())

# ==========================================
# PHASE 2: Train/Test Split
# ==========================================

# 1. Define the target column name
target_column = 'Class'

# 2. Separate features (X) and target (y)
X = data.drop(columns=[target_column])
y = data[target_column]

# 3. Split the data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.2,     # 20% of data goes to the test set
    random_state=42,   # Ensures reproducibility so you get the same split every run
    stratify=y         # Crucial for classification: ensures train and test sets have the same proportion of each obesity class
)

# 4. Verify the splits
print("\n--- Data Split Summary ---")
print(f"Total dataset shape: {data.shape}")
print(f"Training features (X_train) shape: {X_train.shape}")
print(f"Training target (y_train) shape: {y_train.shape}")
print(f"Testing features (X_test) shape: {X_test.shape}")
print(f"Testing target (y_test) shape: {y_test.shape}")