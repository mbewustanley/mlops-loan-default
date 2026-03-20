import os
import pandas as pd
import yaml

from src.logger import logger
from src.exceptions import PipelineException


class DataValidation:

    def __init__(self, data_path, schema_path="config/schema.yaml"):
        self.data_path = data_path
        self.schema_path = schema_path

    def load_schema(self):
        try:
            with open(self.schema_path, "r") as file:
                schema = yaml.safe_load(file)
            return schema
        except Exception as e:
            raise PipelineException(f"Error loading schema: {e}")

    def validate_columns(self, df, schema):
        expected_columns = list(schema["columns"].keys())

        missing_cols = [col for col in expected_columns if col not in df.columns]

        if missing_cols:
            raise PipelineException(f"Missing columns: {missing_cols}")

        logger.info("All required columns are present")
        return True

    def validate(self):
        try:
            logger.info("Starting data validation")

            df = pd.read_csv(self.data_path)
            schema = self.load_schema()

            self.validate_columns(df, schema)

            logger.info("Data validation completed successfully")
            return True

        except Exception as e:
            raise PipelineException(f"Error in data validation: {e}")
        



