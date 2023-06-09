"""
Pipeline from web data to GCS
"""
import os
from datetime import timedelta
from pathlib import Path
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from prefect_gcp.cloud_storage import GcsBucket
from prefect import flow, task

BASE_DIR = '.'
DATASET_NAME = 'spotify-and-youtube'

@task(name="Fetch data from Kaggle", retries=3, cache_expiration=timedelta(days=1))
def fetch() -> None:
    """
    # go to https://www.kaggle.com/settings/account
    # API -> Create New Token
    # mv kaggle.json to project dir
     """
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(
        f'salvatorerastelli/{DATASET_NAME}',
        path=BASE_DIR)

@task(name="Data transform", log_prints=True)
def transform() -> pd.DataFrame:
    """Change duration to minutes from miliseconds, remove miliseconds column."""
    data_frame = pd.read_csv(BASE_DIR+"/"+DATASET_NAME+".zip")
    dfc = data_frame.copy()
    dfc['dur_min']=(dfc['Duration_ms']/1000)/60
    #dfc.drop(['Duration_ms'], axis=1, inplace=True)
    return dfc

@task(name="Write DataFrame to parquet file")
def write_local(data_frame: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    # if there's no directory structure, make ones
    if not os.path.isdir("data"):
        os.makedirs("data", exist_ok=True)
    path = Path(f"data/{dataset_file}.parquet")
    data_frame.to_parquet(path, compression="gzip")
    return path

@task(name="Upload parquet file to GCS", log_prints=True)
def write_gcs(path: Path) -> None:
    """Uploading local parquet file to GCS"""
    # change path to posix type, requires prefect-gcp[cloud_storage]==0.2.4
    # (fix Windows double backslashes to slashes)
    path = Path(path).as_posix()
    opath = path.split("/")[1]
    gcp_cloud_storage_bucket_block = GcsBucket.load(os.environ['GCP_BUCKET'])
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path=f"{path}",
        to_path=f"{opath}"
    )

@task(name="Do cleanups", log_prints=True)
def cleanup():
    """Remove downloaded from Kaggle zip file"""
    os.remove(BASE_DIR+"/"+DATASET_NAME+".zip")

@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    fetch()
    df_transform = transform()
    path = write_local(df_transform, DATASET_NAME)
    write_gcs(path)
    cleanup()

@flow()
def etl_parent_flow():
    """Parent flow"""
    etl_web_to_gcs()

if __name__ == "__main__":
    etl_parent_flow()
