"""ETL GCS to BigQuery"""
from pathlib import Path
from os import environ, remove
import pandas as pd
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect import flow, task

BASE_DIR = '.'
DATASET_NAME = 'spotify-and-youtube'

@task(retries=3, name="Extract from GCS")
def extract_from_gcs() -> Path:
    """Download trip data from GCS"""
    gcs_path = f"{DATASET_NAME}.parquet"
    local_path = "."
    gcs_block = GcsBucket.load(environ['GCP_BUCKET'])
    gcs_block.get_directory(from_path=gcs_path, local_path=local_path)
    return Path(f"{gcs_path}")

@task(name="Data cleaning")
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example - nothing to transform this time"""
    data_frame = pd.read_parquet(path)
    return data_frame

@task(name="Write to Big Query")
def write_bq(data_frame: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""

    gcp_credentials_block = GcpCredentials.load(environ['GCP_CREDENTIALS'])

    data_frame.to_gbq(
        destination_table="sandy.ingest",
        project_id=environ['PROJECT_ID'],
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@task(name="Do cleanups", log_prints=True)
def cleanup():
    """Remove parquet file"""
    remove(DATASET_NAME+".parquet")

@flow(log_prints=True)
def etl_gcs_to_bq() -> int:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs()
    data_frame = transform(path)
    print(f"Rows processed: {len(data_frame)}")
    write_bq(data_frame)
    cleanup()

@flow(log_prints=True)
def etl_parent_flow():
    """Parent flow"""
    etl_gcs_to_bq()

if __name__ == "__main__":
    etl_parent_flow()
