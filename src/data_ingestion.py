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

raw = "https://raw.githubusercontent.com/PacktPublishing/Machine-Learning-for-Finance/master/LendingClub/loan.csv"

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
DATA_URL = "https://raw.githubusercontent.com/selva86/datasets/master/LoanStats3a.csv"


#-----------------------------------------------------------------

class DataIngestion:

    def __init__(self):
        self.raw_data_path = "data/raw"
        self.file_name = "loan_data.csv"

    def download_data(self):
        try:
            logger.info("Starting data ingestion")

            os.makedirs(self.raw_data_path, exist_ok=True)

            file_path = os.path.join(self.raw_data_path, self.file_name)

            logger.info(f"Downloading dataset from {DATA_URL}")

            response = requests.get(DATA_URL)

            if response.status_code != 200:
                raise PipelineException("Failed to download dataset")
            
            with open(file_path, "wb") as f:
                f.write(response.content)

            logger.info(f"Dataset saved at {file_path}")

            return file_path
        
        except Exception as e:
            raise PipelineException(f"Error in data ingestion: {e}")
        

if __name__ == "__main__":
    ingestion = DataIngestion()
    path = ingestion.download_data()

    print(f"Data downloaded to: {path}")