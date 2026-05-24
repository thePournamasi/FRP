import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_preprocessing import DataLoader, DataCleaning

# load dataset
loader = DataLoader("data/obesity_dataset.xlsx")

data = loader.load_data()

# Day 2 cleaning reuse
cleaner = DataCleaning(data)

clean_data = cleaner.clean_data()


# -------------------
# 1. boxplots (detect outliers)
# -------------------

numerical_cols = clean_data.select_dtypes(include=['int64','float64']).columns

for col in numerical_cols:

    plt.figure(figsize=(5,3))

    sns.boxplot(x=clean_data[col])

    plt.title(f"Boxplot of {col}")

    plt.show()



# -------------------
# 2. correlation heatmap
# -------------------

plt.figure(figsize=(10,6))

correlation_matrix = clean_data.corr(numeric_only=True)

sns.heatmap(correlation_matrix, annot=True)

plt.title("Correlation Between Numerical Features")

plt.show()



# -------------------
# 3. influential factors affecting obesity
# -------------------

plt.figure(figsize=(6,4))

sns.boxplot(x="Class", y="Age", data=clean_data)

plt.title("Obesity Level vs Age")

plt.xticks(rotation=45)

plt.show()



plt.figure(figsize=(6,4))

sns.boxplot(x="Class", y="Height", data=clean_data)

plt.title("Obesity Level vs Height")

plt.xticks(rotation=45)

plt.show()



plt.figure(figsize=(6,4))

sns.countplot(x="Consumption_of_Fast_Food", hue="Class", data=clean_data)

plt.title("Fast Food Consumption vs Obesity Level")

plt.show()



plt.figure(figsize=(6,4))

sns.countplot(x="Physical_Excercise", hue="Class", data=clean_data)

plt.title("Physical Exercise vs Obesity Level")

plt.show()
