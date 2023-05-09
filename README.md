# Querry Flow

Web application using FastAPI that allows users to upload CSV files to Google Cloud Storage and query BigQuery tables to retrieve data based on the uploaded file.

## Requirements:

- python
- pip
- [gcloud service account key](https://cloud.google.com/iam/docs/keys-create-delete#iam-service-account-keys-create-gcloud)

## How to run

### Virtual environment

- `/> python -m venv .venv`
- `/> source .venv/bin/activate`
- `/> python -m pip install -r requirements.txt`

### Run

- `uvicorn fast_api:app --reload`
