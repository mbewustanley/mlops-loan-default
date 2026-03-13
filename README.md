# mlops-loan-default

# MLOps Loan Default Prediction Pipeline

## Overview

This project implements a **production-style end-to-end MLOps pipeline** for predicting the likelihood that a borrower will default on a loan.

The goal is to simulate how real ML teams design, build, deploy, and monitor machine learning systems in production.

Pipeline lifecycle:

Data Ingestion → Data Validation → Feature Engineering → Model Training → Experiment Tracking → Model Registry → API Deployment → Monitoring → CI/CD

---

# Project Setup

Follow the steps below to set up the project locally.

---

# 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/mlops-loan-default.git
cd mlops-loan-default
```

---

# 2. Create Conda Environment

This project uses **Conda** for environment management.

Create a new environment:

```bash
conda create -n mlops-loan-default python=3.10
```

Activate the environment:

```bash
conda activate mlops-loan-default
```

Verify Python version:

```bash
python --version
```

---

# 3. Install Dependencies

Install core libraries using conda:

```bash
conda install pandas numpy scikit-learn
```

Install remaining libraries using pip:

```bash
pip install xgboost
pip install mlflow
pip install fastapi uvicorn
pip install dvc
pip install prefect
pip install evidently
```

Freeze dependencies:

```bash
pip freeze > requirements.txt
```

Export the conda environment:

```bash
conda env export > environment.yml
```

---

# 4. Initialize Data Version Control (DVC)

Initialize DVC:

```bash
dvc init
```

Commit the changes:

```bash
git add .
git commit -m "Initialize project structure and DVC"
```

Push to GitHub:

```bash
git push origin main
```

---

# 5. Project Structure

```
mlops-loan-default/

data/
   raw/
   processed/

notebooks/

src/
   data_ingestion.py
   data_validation.py
   preprocessing.py
   feature_engineering.py
   train.py
   evaluate.py

   pipeline/
       training_pipeline.py

api/
   main.py

tests/
configs/
artifacts/

.github/workflows/

Dockerfile
requirements.txt
environment.yml
dvc.yaml
README.md
```

## create structure folder

```
mkdir data
mkdir data/raw
mkdir data/processed

mkdir notebooks
mkdir src
mkdir src/pipeline
mkdir src/models

mkdir api
mkdir tests
mkdir artifacts
mkdir configs

mkdir .github
mkdir .github/workflows
```

## create key files

```
touch requirements.txt
touch Dockerfile
touch dvc.yaml
```

## create source modules

```
touch src/data_ingestion.py
touch src/data_validation.py
touch src/preprocessing.py
touch src/feature_engineering.py
touch src/train.py
touch src/evaluate.py

touch src/pipeline/training_pipeline.py
```

## create API starter

```
touch api/main.py
```

---

# 6. Technology Stack

**Core ML**

- Python
- Pandas
- Scikit-learn
- XGBoost

**Experiment Tracking**

- MLflow

**Data Versioning**

- DVC

**Pipeline Orchestration**

- Prefect

**Model Serving**

- FastAPI

**Containerization**

- Docker

**CI/CD**

- GitHub Actions

**Monitoring**

- Evidently AI

---

# 7. Development Phases

Phase 1 — Project Setup
Phase 2 — Data Pipeline
Phase 3 — Model Development
Phase 4 — Experiment Tracking
Phase 5 — Deployment
Phase 6 — CI/CD
Phase 7 — Monitoring

---

# Next Development Step

The next step is implementing the **data ingestion pipeline** which will:

- Download the LendingClub dataset
- Store it in `data/raw`
- Track the dataset using DVC
- Prepare the data for validation and preprocessing
