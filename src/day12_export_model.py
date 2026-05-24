import joblib
import os
import sys
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from data_preprocessing import DataLoader, DataCleaning
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

print("--- Starting Final Model Export ---")

# 1. Load and Clean
base_dir = os.path.dirname(script_dir)
data_path = os.path.join(base_dir, "data", "clean_obesity_dataset.csv")
data = DataLoader(data_path).load_data()

# Clean the dataset before splitting to remove NaNs and duplicates
cleaned_data = DataCleaning(data).clean_data()

# Ensure the target column contains only valid numeric class labels
cleaned_data['Class'] = pd.to_numeric(cleaned_data['Class'], errors='coerce')
cleaned_data = cleaned_data.dropna(subset=['Class'])
cleaned_data['Class'] = cleaned_data['Class'].astype(int)
cleaned_data = cleaned_data[cleaned_data['Class'].isin([1, 2, 3, 4])]

X = cleaned_data.drop(columns=['Class'])
y = cleaned_data['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==========================================
# 2. TRAIN THE ULTIMATE MODEL
# ==========================================
print("Training the final, optimized model...")

#  UPDATE THESE SETTINGS! 
# Look at the terminal output from Day 11. Put your best parameters here.
# Example: If Day 11 said {'max_depth': 20, 'min_samples_split': 2, 'n_estimators': 100}

final_model = RandomForestClassifier(
    max_depth=None,           # Replace with the best max_depth
    min_samples_split=2,      # Replace with the best min_samples_split
    n_estimators=200,         # Replace with  best n_estimators
    random_state=42
)

final_model.fit(X_train, y_train)

# ==========================================
# 3. SAVE TO HARD DRIVE
# ==========================================
# Save the trained model in the project root 'models' folder
model_dir = os.path.join(base_dir, "models")
os.makedirs(model_dir, exist_ok=True)
model_filename = os.path.join(model_dir, "obesity_rf_model.joblib")

joblib.dump(final_model, model_filename)

print("==========================================")
print(f"SUCCESS! Model saved to: {model_filename}")
print("==========================================")
print("This file contains your trained AI. It is now ready to be deployed!")

print(f"SUCCESS! Model saved to: {model_filename}")
print("==========================================")
print("This file contains your trained AI. It is now ready to be deployed!")
