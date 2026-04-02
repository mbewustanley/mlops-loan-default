import os
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from src.logger import logging
from src.exceptions import PipelineException


class FeatureSelector:
    def __init__(self, data_path, output_path, feature_path):
        self.data_path = data_path
        self.output_path = output_path
        self.feature_path = feature_path

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            logging.info("Data loaded for feature selection")
            return df
        except Exception as e:
            raise PipelineException(f"Error loading data: {e}")

    def select_features(self, df):
        try:
            X = df.drop(columns=["loan_status"])
            y = df["loan_status"]

            model = RandomForestClassifier(
                n_estimators=50,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )

            model.fit(X, y)

            importances = model.feature_importances_
            feature_names = X.columns

            feature_importance_df = pd.DataFrame({
                "feature": feature_names,
                "importance": importances
            }).sort_values(by="importance", ascending=False)

            # Keep top N features
            top_n = 30
            selected_features = feature_importance_df.head(top_n)["feature"].tolist()

            logging.info(f"Selected top {top_n} features")

            return selected_features

        except Exception as e:
            raise PipelineException(f"Error selecting features: {e}")

    def save_outputs(self, df, selected_features):
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

            df_selected = df[selected_features + ["loan_status"]]
            df_selected.to_csv(self.output_path, index=False)

            with open(self.feature_path, "w") as f:
                json.dump(selected_features, f, indent=4)

            logging.info("Feature selection outputs saved")

        except Exception as e:
            raise PipelineException(f"Error saving selected features: {e}")

    def run(self):
        try:
            df = self.load_data()

            selected_features = self.select_features(df)

            self.save_outputs(df, selected_features)

            return self.output_path

        except Exception as e:
            raise PipelineException(f"Error in feature selection pipeline: {e}")