import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import DataLoader, DataCleaning

print("--- Starting EDA Compilation & Finalization ---")

# ==========================================
# 1. SETUP PROJECT FOLDERS
# ==========================================
# This automatically creates a 'reports' folder to keep our project organized
os.makedirs("reports", exist_ok=True)
os.makedirs("reports/graphs", exist_ok=True)

# ==========================================
# 2. LOAD & CLEAN DATA
# ==========================================
print("Loading and cleaning data...")
loader = DataLoader("data/obesity_dataset.xlsx")
raw_data = loader.load_data()
clean_data = DataCleaning(raw_data).clean_data()

# ==========================================
# 3. GENERATE & SAVE TEXT REPORT
# ==========================================
print("Generating written statistical report...")
report_path = "reports/dataset_summary.txt"

# We open a text file and write our analysis directly into it
with open(report_path, "w") as file:
    file.write("=== OBESITY DATASET: EDA SUMMARY REPORT ===\n\n")
    file.write(f"Final Cleaned Rows: {clean_data.shape[0]}\n")
    file.write(f"Final Cleaned Columns: {clean_data.shape[1]}\n\n")
    
    file.write("--- Missing Values Check ---\n")
    file.write(clean_data.isnull().sum().to_string() + "\n\n")
    
    file.write("--- Detailed Statistical Summary ---\n")
    file.write(clean_data.describe().to_string() + "\n")

# ==========================================
# 4. GENERATE & SAVE GRAPHS
# ==========================================
print("Saving graphs to folder (running silently in background)...")

# Plot 1: Obesity Level Distribution
plt.figure(figsize=(8,5))
sns.countplot(x="Class", data=clean_data)
plt.title("Obesity Level Distribution")
plt.xticks(rotation=45)
plt.tight_layout() # Ensures labels don't get cut off
plt.savefig("reports/graphs/1_obesity_distribution.png")
plt.close() # Closes the plot so it doesn't pop up and pause the script

# Plot 2: Correlation Heatmap
plt.figure(figsize=(10,8))
sns.heatmap(clean_data.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("reports/graphs/2_correlation_heatmap.png")
plt.close()

# Plot 3: Age vs Height Scatter
plt.figure(figsize=(8,5))
sns.scatterplot(x="Age", y="Height", hue="Class", data=clean_data)
plt.title("Age vs Height by Obesity Level")
plt.tight_layout()
plt.savefig("reports/graphs/3_age_height_scatter.png")
plt.close()

# ==========================================
# 5. FINALIZE DATASET FOR MACHINE LEARNING
# ==========================================
print("Exporting finalized dataset...")
final_data_path = "data/clean_obesity_dataset.csv"

# Save as CSV without the row numbers (index=False)
clean_data.to_csv(final_data_path, index=False)

print("\n==========================================")
print("SUCCESS! EDA Phase Complete.")
print("==========================================")
print(f"- Written Report saved to: {report_path}")
print("- Analysis Graphs saved to: reports/graphs/")
print(f"- ML-Ready Dataset saved to: {final_data_path}")

