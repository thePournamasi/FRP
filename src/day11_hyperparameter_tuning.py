from data_preprocessing import DataLoader
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("--- Starting Hyperparameter Tuning ---")

# ==========================================
# 1. SETUP DATA
# ==========================================
data_path = "data/obesity_dataset.xlsx"
data = DataLoader(data_path).load_data()

X = data.drop(columns=['Class'])
y = data['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==========================================
# 2. DEFINE THE GRID (The Knobs & Dials)
# ==========================================
# n_estimators: How many trees in the forest?
# max_depth: How deep/complex can each tree get? (Prevents overfitting)
# min_samples_split: How many patients needed to make a new branch?
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

print(f"Testing {len(param_grid['n_estimators']) * len(param_grid['max_depth']) * len(param_grid['min_samples_split'])} different combinations...")

# ==========================================
# 3. RUN THE GRID SEARCH
# ==========================================
rf_base = RandomForestClassifier(random_state=42)

# cv=5 means "Cross-Validation". It double-checks its work 5 times per combination.
# n_jobs=-1 tells the computer to use ALL of its CPU cores to do this faster.
grid_search = GridSearchCV(estimator=rf_base, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

print("\nRunning the search (This may take a minute or two)...\n")
grid_search.fit(X_train, y_train)

# ==========================================
# 4. THE RESULTS
# ==========================================
print("==========================================")
print("🏆 TUNING COMPLETE: BEST SETTINGS FOUND")
print("==========================================")
print(grid_search.best_params_)

# Extract the absolute best model from the search
best_rf_model = grid_search.best_estimator_

# Test the tuned model on the final exam data
y_pred = best_rf_model.predict(X_test)
tuned_accuracy = accuracy_score(y_test, y_pred)

print(f"\nNew Tuned Accuracy: {tuned_accuracy * 100:.2f}%")
