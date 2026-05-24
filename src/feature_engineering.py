from sklearn.preprocessing import LabelEncoder, StandardScaler

class FeatureEngineering:

    def __init__(self, data):
        self.data = data

    def transform(self):

        # TARGET VARIABLE (Obesity level)
        y = self.data['Class']

        # FEATURES
        X = self.data.drop('Class', axis=1)

        # categorical columns encode
        categorical_cols = X.select_dtypes(include=['object']).columns

        le = LabelEncoder()

        for col in categorical_cols:
            X[col] = le.fit_transform(X[col])

        # scale numerical columns
        numerical_cols = X.select_dtypes(include=['int64','float64']).columns

        scaler = StandardScaler()

        X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

        return X, y