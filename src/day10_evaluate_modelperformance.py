from data_preprocessing import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

print("--- Starting Model Evaluation Pipeline ---")

# ==========================================
# 1. LOAD, SPLIT & TRAIN (The Setup)
# ==========================================
print("1. Preparing data and model...")
data_path = "data/obesity_dataset.xlsx"
data = DataLoader(data_path).load_data()

X = data.drop(columns=['Class'])
y = data['Class']

# Recreate the exact same 80/20 split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Quickly retrain the Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# ==========================================
# 2. MAKE PREDICTIONS
# ==========================================
print("2. Running the final exam (Test Data)...\n")
y_pred = rf_model.predict(X_test)

# ==========================================
# 3. EXPLICIT METRIC EVALUATION
# ==========================================
# Using average='weighted' to account for the multiple obesity classes fairly
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print("==========================================")
print("🎯 CORE PERFORMANCE METRICS")
print("==========================================")
print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1-Score:  {f1 * 100:.2f}%")
print("==========================================\n")

print("Detailed Classification Report:")
print(classification_report(y_test, y_pred))
