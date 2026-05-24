import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from data_preprocessing import DataLoader, DataCleaning

# load data
loader = DataLoader("data/obesity_dataset.xlsx")

data = loader.load_data()


# Day 2 cleaning
cleaner = DataCleaning(data)

clean_data = cleaner.clean_data()


# encode categorical columns
encoded_data = clean_data.copy()

categorical_cols = encoded_data.select_dtypes(include=['object']).columns

le = LabelEncoder()

for col in categorical_cols:
    encoded_data[col] = le.fit_transform(encoded_data[col])


# separate X and y
X = encoded_data.drop("Class", axis=1)

y = encoded_data["Class"]


# feature importance using Random Forest
model = RandomForestClassifier()

model.fit(X, y)


importance = pd.Series(model.feature_importances_, index=X.columns)

importance = importance.sort_values(ascending=False)


print("\nFeature Importance:\n")

print(importance)