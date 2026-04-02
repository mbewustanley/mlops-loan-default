## Evaluate the model:
# this stage should
# - load the trained model.pkl
# - load the test data
# - generate predictions on the test data
# - evaluate the model on the test data and compute evaluation metrics (e.g., accuracy, precision, recall, F1-score)
# - save the evaluation results for tracking and reproducibility
# - optional; compare against a baseline model

"""
we will;
save metrics as JSON
Log everything
Keep it DVC friendly
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_auc_score)
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exceptions import PipelineException


class ModelEvaluation:
    def __init__(self, data_path, model_path, metrics_path):
        self.data_path = data_path
        self.model_path = model_path
        self.metrics_path = metrics_path


    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            logging.info("Processed data loaded for evaluation")
            return df
        except Exception as e:
            raise PipelineException(f"Error loading processed data: {e}")


    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)

            logging.info("Trained model loaded for evaluation")
            return model
        except Exception as e:
            raise PipelineException(f"Error loading model: {e}")


    def prepare_data(self, df):
        try:
            X = df.drop(columns=["loan_status"])
            y = df["loan_status"]

            logging.info('Implementing Train test split for evaluation')

            _, X_test, _, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            return X_test, y_test

        except Exception as e:
            raise PipelineException(f"Error preparing evaluation data: {e}")

    def evaluate(self, model, X_test, y_test):
        try:
            y_probs = model.predict_proba(X_test)[:, 1]

            thresholds = np.arange(0.1, 0.9, 0.05)
            best_threshold = 0
            best_f1 = 0

            for t in thresholds:
                y_pred = (y_probs > t).astype(int)
                score = f1_score(y_test, y_pred)

                if score > best_f1:
                    best_f1 = score
                    best_threshold = t
            print(f"Best threshold: {best_threshold:.2f} with F1-score: {best_f1:.4f}")

            y_pred = (y_probs > best_threshold).astype(int)

            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1": f1_score(y_test, y_pred),
                "roc_auc": roc_auc_score(y_test, y_probs)
            }
            
            cm = confusion_matrix(y_test, y_pred)
            logging.info(f"Confusion Matrix:\n{cm}")

            logging.info("Model evaluation completed successfully")
            return metrics

        except Exception as e:
            raise PipelineException(f"Error during model evaluation: {e}")

    def save_metrics(self, metrics):
        try:
            os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)

            with open(self.metrics_path, 'w') as f:
                json.dump(metrics, f, indent=4)

            logging.info(f"Evaluation metrics saved at {self.metrics_path}")

        except Exception as e:
            raise PipelineException(f"Error saving evaluation metrics: {e}")

    def run(self):
        try:
            df = self.load_data()
            model = self.load_model()

            X_test, y_test = self.prepare_data(df)

            metrics = self.evaluate(model, X_test, y_test)
            
            self.save_metrics(metrics)
            
            return self.metrics_path
        except Exception as e:
            raise PipelineException(f"Error in evaluation pipeline: {e}")
