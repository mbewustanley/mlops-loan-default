# Model Training Pipeline

# This will:

# Train baseline ML models
# Save trained artifacts
# Integrate with DVC pipeline
# Prepare for experiment tracking (MLflow)


import os
import time
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from src.logger import logging
from src.exceptions import PipelineException


class ModelTrainer:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.model_path = model_path

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            logging.info("Processed data loaded for training")

            # sample a bit of the huge dataset
            df = df.sample(n=100000, random_state=42)
            logging.info(f"dataframe sampled to shape: {df.shape}")
            return df
        except Exception as e:
            raise PipelineException(f"Error loading data: {e}")

    def split_data(self, df):
        try:
            X = df.drop(columns=["loan_status"])
            y = df["loan_status"]

            logging.info('Implementing Train test split')

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            return X_train, X_test, y_train, y_test

        except Exception as e:
            raise PipelineException(f"Error splitting data: {e}")

    def train_model(self, X_train, y_train):
        try:
            logging.info("Attempting model training")
            start_time = time.time()
            model = RandomForestClassifier(
                n_estimators=50,
                max_depth=10,
                min_samples_split=10,
                random_state=42,
                n_jobs=-1)
            model.fit(X_train, y_train)
            end_time = time.time()

            print(f"Training time: {end_time - start_time:.4f} seconds")
            logging.info("Model training completed")
            return model

        except Exception as e:
            raise PipelineException(f"Error training model: {e}")

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

            with open(self.model_path, "wb") as f:
                pickle.dump(model, f)

            logging.info(f"Model saved at {self.model_path}")

        except Exception as e:
            raise PipelineException(f"Error saving model: {e}")

    def train(self):
        try:
            df = self.load_data()
            print(df['emp_length'].unique)

            X_train, X_test, y_train, y_test = self.split_data(df)

            model = self.train_model(X_train, y_train)

            self.save_model(model)

            return self.model_path

        except Exception as e:
            raise PipelineException(f"Error in training pipeline: {e}")