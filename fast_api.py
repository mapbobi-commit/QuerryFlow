from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from google.cloud import storage, bigquery


class Querry(BaseModel):
    querry: str


app = FastAPI()
client = bigquery.Client()


@app.post("/uploadfile/{csv_file_id}")
def create_upload_file(csv_file_id, csv_file: UploadFile):
    csv_content = csv_file.file.read()
    print(csv_file.filename.split(".")[-1])

    if csv_file.filename.split(".")[-1] != "csv":
        raise HTTPException(status_code=404, detail="The file you chose is not a csv")

    # Uploads file to Google Cloud Storage
    storage_client = storage.Client()
    bucket_name = storage_client.bucket("api_tester")
    blob = bucket_name.blob(csv_file_id)
    generation_match_precondition = 0

    blob.upload_from_string(csv_content)

    # Constructs the file in BigQuery
    table_id = f"omniproject-51.api_testing.{csv_file_id}"

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
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


@app.post("/make_querry")
def querry(item: Querry):
    query = item.querry
    querry_job = client.query(query)
    try:
        data = querry_job.result()
    except:
        raise HTTPException(status_code=404, detail="The querry failed")
    rows = list(data)

    return rows
