from typing import Annotated
from fastapi import FastAPI, File, HTTPException
from pydantic import BaseModel
from google.cloud import storage, bigquery
from io import StringIO
import csv


class Querry(BaseModel):
    querry: str


app = FastAPI()
client = bigquery.Client()


@app.post("/uploadfile/{csv_file_id}")
def create_upload_file(csv_file_id, csv_file: Annotated[bytes, File()]):
    # Uploads file to Google Cloud Storage
    storage_client = storage.Client()
    bucket_name = storage_client.bucket("api_tester")
    blob = bucket_name.blob(csv_file_id)
    generation_match_precondition = 0

    blob.upload_from_string(csv_file)

    # Constructs the file in BigQuery
    table_id = f"omniproject-51.api_testing.{csv_file_id}"

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://api_tester/{csv_file_id}"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    client.get_table(table_id)


@app.post("/make_querry")
def querry(item: Querry):
    query = item.querry
    querry_job = client.query(query)
    data = querry_job.result()
    rows = list(data)

    return rows
