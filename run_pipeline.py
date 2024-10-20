import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

from pipelines.training_pipeline import train_pipeline

TAG = "run_pipeline.py"

if __name__ == "__main__":
    train_pipeline(bucket_name="ruby_mlops_test", source_blob_name="raw_data/digits", test_size_percent=0.7)