import pandas as pd
import os

from src.logger import logger
from src.exceptions import PipelineException


class DataTransformation:

    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path, low_memory=False)
            logger.info("Data loaded for transformation")
            return df
        except Exception as e:
            raise PipelineException(f"Error loading data: {e}")
        

    def clean_int_rate(self, df):
        try:
            df = df.copy()

            # Convert everything to string first
            df['int_rate'] = df['int_rate'].astype(str)

            # Remove % sign
            df['int_rate'] = df['int_rate'].str.replace('%', '', regex=False)

            # Convert to float safely
            df['int_rate'] = pd.to_numeric(df['int_rate'], errors='coerce')

            return df

        except Exception as e:
            raise PipelineException(f"Error cleaning int_rate: {e}")
        
    def process_target(self, df):
        try:
            df = df.copy()
            # keep only relevant classes
            df = df[df['loan_status'].isin(['Fully Paid', 'Charged Off'])]

            # map to binary
            df.loc[:, 'loan_status'] = df['loan_status'].map({
                'Fully Paid': 0,
                'Charged Off': 1
            })

            logger.info("Target variable processed")
            return df
        except Exception as e:
            raise PipelineException(f"Error processing target: {e}")

    def handle_missing_values(self, df):  # very aggressive and should be changed to a better way to address missing values
        try:
            df = df.copy()

            #change when you can abeg
            df = df.dropna(subset=['loan_status'])
            logger.info("Missing values dropped")

            return df
        except Exception as e:
            raise PipelineException(f"Error handling missing values: {e}")

    def save_data(self, df):
        try:
            output_path = "data/processed"
            os.makedirs(output_path, exist_ok=True)

            file_path = os.path.join(output_path, "processed_data.csv")
            df.to_csv(file_path, index=False)

            logger.info(f"Processed data saved at {file_path}")
            return file_path
        except Exception as e:
            raise PipelineException(f"Error saving transformed data: {e}")

    def transform(self):
        try:
            df = self.load_data()

            df = self.process_target(df)
            df = self.clean_int_rate(df)
            df = self.handle_missing_values(df)

            logger.info(f"Final dataset shape: {df.shape}")

            return self.save_data(df)

        except Exception as e:
            raise PipelineException(f"Error in data transformation: {e}")