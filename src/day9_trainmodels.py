from data_preprocessing import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

print("--- Starting Model Training Pipeline ---")

# ==========================================
# 1. LOAD & SPLIT DATA 
# ==========================================
print("1. Loading and splitting data...")
data_path = "data/obesity_dataset.xlsx"
data = DataLoader(data_path).load_data()

X = data.drop(columns=['Class'])
y = data['Class']

# Recreating the exact same 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==========================================
# 2. TRAIN THE MODEL
# ==========================================
print("2. Training the Random Forest model...")
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

print("\n✅ Model training complete!")
print("Run day10_model_evaluation.py to see the detailed performance grades.")

