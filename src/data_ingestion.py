""" src/data_ingestion.py should ONLY handle:
Downloading / loading the dataset
Saving the raw dataset
Logging the process
Basic sanity checks
Preparing output for the validation stage

It should NOT:
clean the data
engineer features
split train/test
Those belong to later modules."""

# For Loan Default Prediction, a common dataset used in production demos is:
# LendingClub Loan Data
# loaded from a public hosted csv, this keeps the pipeline reproducible

#raw = "https://raw.githubusercontent.com/PacktPublishing/Machine-Learning-for-Finance/master/LendingClub/loan.csv"

# in real prod, we might need to pull from an s3, api, data lake, or data warehouse

"""
Data Ingestion Pipeline

1️⃣ Create raw data directory if not present
2️⃣ Download dataset
3️⃣ Save dataset locally
4️⃣ Validate download success
5️⃣ Log ingestion steps
6️⃣ Return file path to next pipeline stage
"""


#####################################################################################

import os
import sys
import pandas as pd
import requests

from src.logger import logger
from src.exceptions import PipelineException

# ___________LENDING CLUB DATA SOURCE_____________

#DATA_URL = "https://raw.githubusercontent.com/PacktPublishing/Machine-Learning-for-Finance/master/LendingClub/loan.csv"
#DATA_URL = "https://raw.githubusercontent.com/selva86/datasets/master/LoanStats3a.csv"



## kAGGLE DATA SOURCE ---------------------

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]

import kagglehub
from kagglehub import KaggleDatasetAdapter




#print("First 5 records:", df.head())


#-----------------------------------------------------------------

class DataIngestion:

    def __init__(self):
        self.raw_data_path = "data/raw"
        self.file_name = "loan_data.csv"


    def save(self, df):
        try:
            os.makedirs(self.raw_data_path, exist_ok=True)
            os_file_path = os.path.join(self.raw_data_path, self.file_name)

            # save dataset to self.raw_data_path
            logger.info(f"attempting to save file to {os_file_path}")
            df.to_csv(os_file_path, index=False)

            logger.info(f"Dataset saved at {os_file_path}")

        except Exception as e:
            raise PipelineException(f"Error saving dataset to file path: {e} ")

        return os_file_path
    
    def read_csv_with_fallback(self, file_path):
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

        for enc in encodings:
            try:
                logger.info(f"Trying encoding: {enc}")
                df = pd.read_csv(file_path, encoding=enc, low_memory=False)
                logger.info(f"Successfully read file with encoding: {enc}")
                return df
            except Exception as e:
                logger.warning(f"Failed with encoding {enc}: {e}")

        raise PipelineException("All encoding attempts failed")

        
    def download_data(self):
        try:
            logger.info("starting data ingestion")

            file_name = "loan.csv"

            logger.info("Downloading dataset from Kaggle...")

            # Step 1: download dataset locally (returns folder path)
            dataset_path = kagglehub.dataset_download(
                "adarshsng/lending-club-loan-data-csv"
            )

            file_path = os.path.join(dataset_path, file_name)

            logger.info(f"Dataset downloaded to {file_path}")

            # Step 2: robust CSV reader
            df = self.read_csv_with_fallback(file_path)

            logger.info("Dataset successfully loaded into DataFrame")
            print("First 5 records:\n", df.head())

            # Step 3: save
            os_file_path = self.save(df)

            logger.info(f"Dataset shape: {df.shape}")
            logger.info(f"Columns: {list(df.columns)}")

            return os_file_path
        


        except Exception as e:
            raise PipelineException(f"Error in data ingestion: {e}")




from src.data_validation import DataValidation

if __name__ == "__main__":
    ingestion = DataIngestion()
    data_path = ingestion.download_data()

    validator = DataValidation(data_path)
    validator.validate()

    print(f"Data downloaded to: {data_path}")
    print("Pipeline completed successfully")