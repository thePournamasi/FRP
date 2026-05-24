import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Import the 3 algorithms we are fighting against each other
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

print("--- Starting Algorithm Benchmark ---")

# ==========================================
# 1. LOAD AND PERFECTLY CLEAN THE DATA
# ==========================================
# (Using the bulletproof cleaning block we created earlier)
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
data_path = os.path.join(base_dir, "data", "clean_obesity_dataset.csv")

data = pd.read_csv(data_path)
data.columns = data.columns.str.strip()
data = data.dropna()
data = data[data['Class'] != 'Class']

X = data.drop(columns=['Class'])
y = data['Class']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==========================================
# 2. INITIALIZE THE 3 MODELS
# ==========================================
# Note: Logistic Regression needs a high 'max_iter' or it gives up before finishing the math
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42)
}

# ==========================================
# 3. TRAIN, TEST, AND RECORD SCORES
# ==========================================
results = {}

print("\n--- Training Results ---")
for name, model in models.items():
    # Train the model
    model.fit(X_train, y_train)
    
    # Test the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions) * 100
    
    # Save and print the score
    results[name] = accuracy
    print(f"{name}: {accuracy:.2f}% Accuracy")

# ==========================================
# 4. GENERATE A GRAPH FOR YOUR REPORT
# ==========================================
plt.figure(figsize=(10, 6))
colors = ['#ff9999', '#66b3ff', '#99ff99'] # Red, Blue, Green
bars = plt.bar(results.keys(), results.values(), color=colors)

# Add title and labels
plt.title('Algorithm Accuracy Comparison (Obesity Classification)', fontsize=14, fontweight='bold')
plt.ylabel('Accuracy (%)', fontsize=12)
plt.ylim(0, 105) # Give the graph some headroom

# Add the exact percentage numbers on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom', fontweight='bold')

# Save the image to your project folder
graph_filename = "model_comparison_graph.png"
plt.savefig(graph_filename)
print(f"\nSUCCESS! Graph saved as: {graph_filename}")
