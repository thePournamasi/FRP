import os
import pandas as pd

class DataLoader:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        extension = os.path.splitext(self.path)[1].lower()
        if extension == '.csv':
            data = pd.read_csv(self.path)
        elif extension in ('.xls', '.xlsx'):
            data = pd.read_excel(self.path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        return data


class DataCleaning:

    def __init__(self, data):
        self.data = data

    def clean_data(self):

        # remove duplicate rows
        self.data = self.data.drop_duplicates()

        # remove missing values
        self.data = self.data.dropna()

        # reset index
        self.data = self.data.reset_index(drop=True)

        return self.data
    