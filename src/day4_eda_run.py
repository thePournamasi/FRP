import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_preprocessing import DataLoader, DataCleaning

# load data
loader = DataLoader("data/obesity_dataset.xlsx")

data = loader.load_data()

# cleaning (Day 2 reuse)
cleaner = DataCleaning(data)

clean_data = cleaner.clean_data()

# -------------------
# 1. statistical summary
# -------------------

print("\nStatistical Summary:")
print(clean_data.describe())

print("\nData Info:")
print(clean_data.info())


# -------------------
# 2. histograms (distribution)
# -------------------

clean_data.hist(figsize=(12,10))

plt.suptitle("Feature Distributions")

plt.show()


# -------------------
# 3. count plots (categorical distribution)
# -------------------

plt.figure(figsize=(6,4))

sns.countplot(x="Class", data=clean_data)

plt.title("Obesity Level Distribution")

plt.xticks(rotation=45)

plt.show()


# -------------------
# 4. relationship between variables
# -------------------

plt.figure(figsize=(6,4))

sns.scatterplot(x="Age", y="Height", hue="Class", data=clean_data)

plt.title("Age vs Height by Obesity Level")

plt.show()


# correlation heatmap (numerical relation)
plt.figure(figsize=(10,6))

sns.heatmap(clean_data.corr(numeric_only=True), annot=True)

plt.title("Correlation Heatmap")

plt.show()