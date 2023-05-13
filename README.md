# Querry Flow

Web application using FastAPI that allows users to upload CSV files to Google Cloud Storage and query BigQuery tables to retrieve data based on the uploaded file.

## Requirements:

- python
- pip
- [gcloud service account key](https://cloud.google.com/docs/authentication/api-keys)

## How to run

### Virtual environment

- `$ python -m venv .venv`
- `$ source .venv/bin/activate`
- `$ python -m pip install -r requirements.txt`

### Run

- `uvicorn fast_api:app --reload`
- `go to the site/docs and run tests`
