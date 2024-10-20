import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

import os
from google.cloud import storage
from zenml import step

TAG = "ingest_data.py"

class IngestData:
    '''
    Class to ingest data.
    '''

    def __init__(self, bucket_name: str, source_blob_name: str) -> None:
        '''
        Constructor for the class.

        Args:
            bucket_name: str: Name of the bucket.
            source_blob_name: str: Name of the source blob.

        Returns:
            None
        '''

        self.bucket_name = bucket_name
        self.source_blob_name = source_blob_name

    def run(self) -> None:
        '''
        Read data from the bucket.
        '''

        try:
            if not os.path.exists("data"):
                os.makedirs("data")
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(self.bucket_name)
            blobs = bucket.list_blobs(prefix=self.source_blob_name)
            for blob in blobs:
                if not blob.name.endswith("/"):
                    filename = blob.name.split("/")[-1]
                    destination_file_path = os.path.join("data", filename)
                    destination_file_path_corrected = destination_file_path.replace('.', '-')
                    if os.path.exists(destination_file_path_corrected):
                        logger.info(f"File {destination_file_path_corrected} already exists, skipping", extra={"tag": TAG})
                        continue
                    blob.download_to_filename(destination_file_path_corrected)
                    logger.info(f"Downloaded {blob.name} to {destination_file_path_corrected}", extra={"tag": TAG})

        except Exception as e:
            logger.error(f"Error in running the ingestion: {e}", extra={"tag": TAG})
            raise e
        
@step
def ingest_data(bucket_name: str, source_blob_name: str) -> str:
    '''
    Function to ingest data.

    Args:
        bucket_name: str: Name of the bucket.
        source_blob_name: str: Name of the source blob.

    Returns:
        str: Path to the raw data.
    '''

    try:
        ingest_data_obj = IngestData(bucket_name, source_blob_name)
        ingest_data_obj.run()
        return "data"
    
    except Exception as e:
        logger.error(f"Error in running the ingestion: {e}", extra={"tag": TAG})
        raise e