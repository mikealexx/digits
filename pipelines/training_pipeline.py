import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

from zenml import pipeline
from steps.ingest_data import ingest_data
from steps.clean_data import clean_data
from steps.train_model import train_model
from steps.evaluate_model import evaluate_model

TAG = "training_pipeline.py"

@pipeline(enable_cache=True)
def train_pipeline(bucket_name: str, source_blob_name: str, train_size_percentage: float = 1, test_size_percent: float = 0.3):
    '''
    Pipeline to train the model.

    Args:
        bucket_name: str: Name of the bucket.
        source_blob_name: str: Name of the source blob.
        train_size_percentage: float: Percentage of the training data (default: 1).
        test_size_percent: float: Percentage of the testing data (default: 0.3).

    Returns:
        None
    '''

    raw_data_path = ingest_data(bucket_name, source_blob_name)
    X_train, y_train, X_test, y_test = clean_data(raw_data_path, train_size_percentage, test_size_percent)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)