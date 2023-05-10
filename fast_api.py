from fastapi import FastAPI, UploadFile, HTTPException, Form
from pydantic import BaseModel
from google.cloud import storage, bigquery
from typing import Annotated


class Gcloud_info(BaseModel):
    gcloud_service_account_key: str
    csv_file_id_or_querry: str


app = FastAPI()


@app.post("/uploadfile/")
def create_upload_file(
    gcloud_service_api_key: Annotated[str, Form()],
    csv_file_id: Annotated[str, Form()],
    csv_file: UploadFile,
):
    client = bigquery.Client()

    csv_content = csv_file.file.read()

    if csv_file.filename.split(".")[-1] != "csv":
        raise HTTPException(status_code=504, detail="The file you chose is not a csv")

    # Uploads file to Google Cloud Storage
    storage_client = storage.Client(
        client_options={
            "quota_project_id": "omniproject-51",
            "api_key": gcloud_service_api_key,
        }
    )
    bucket_name = storage_client.bucket("api_tester")
    blob = bucket_name.blob(csv_file_id)

    blob.upload_from_string(csv_content)

    # Constructs the file in BigQuery
    table_id = f"omniproject-51.api_testing.{csv_file_id}"

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = f"gs://api_tester/{csv_file_id}"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    try:
        load_job.result()
    except:
        raise HTTPException(
            status_code=404, detail="The csv file has incosistencies or is not a csv"
        )
    client.get_table(table_id)
    return "succesfull upload"


@app.post("/make_querry/")
def querry(
    querry: Annotated[str, Form()], gcloud_service_api_key: Annotated[str, Form()]
):
    client = bigquery.Client(
        client_options={
            "quota_project_id": "omniproject-51",
            "api_key": gcloud_service_api_key,
        }
    )

    querry_job = client.query(querry)
    try:
        data = querry_job.result()
    except:
        raise HTTPException(status_code=404, detail="The querry failed")
    rows = list(data)

    return rows
