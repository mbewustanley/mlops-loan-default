import argparse
from src.data_ingestion import DataIngestion
from src.data_validation import DataValidation
from src.data_transformation import DataTransformation


def run_ingestion():
    ingestion = DataIngestion()
    data_path = ingestion.download_data()
    return data_path


def run_validation(data_path):
    validator = DataValidation(data_path)
    validator.validate()
    return data_path


def run_transformation(data_path):
    transformer = DataTransformation(data_path)
    processed_path = transformer.transform()
    return processed_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True)

    args = parser.parse_args()

    if args.stage == "ingest":
        output = run_ingestion()

    elif args.stage == "validate":
        # DVC will pass dependency via file path
        output = run_validation("data/raw/loan_data.csv")

    elif args.stage == "transform":
        output = run_transformation("data/raw/loan_data.csv")

    else:
        raise ValueError("Invalid stage")

    print(f"Stage {args.stage} completed: {output}")