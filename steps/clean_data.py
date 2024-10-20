import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

from zenml import step
import numpy as np
from typing_extensions import Tuple
from typing import Annotated
from mnist import MNIST

TAG = "clean_data.py"

@step
def clean_data(raw_data_path: str, train_size_percentage: float = 1, test_size_percent: float = 0.3) -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_test"]
]:
    '''
    Function to cleanand prepare the data.

    Args:
        raw_data_path: str: Path to the raw data.
        train_size_percentage: float: Percentage of the training data (default: 1).
        test_size_percent: float: Percentage of the testing data (default: 0.3).

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Cleaned data.
    '''

    try:
        logger.info(f"Loading MNIST data from {raw_data_path}", extra={"tag": TAG})
        mndata = MNIST(raw_data_path)

        logger.info("Loading training data", extra={"tag": TAG})
        X_train, y_train = mndata.load_training()
        X_train = np.array(X_train).reshape(-1, 28*28)
        X_train = X_train[:int(train_size_percentage*len(X_train))]
        y_train = np.array(y_train)
        y_train = y_train[:int(train_size_percentage*len(y_train))]
        logger.info(f"Loaded {len(X_train)} training samples", extra={"tag": TAG})

        logger.info("Loading testing data", extra={"tag": TAG})
        X_test, y_test = mndata.load_testing()
        X_test = np.array(X_test).reshape(-1, 28*28)
        X_test = X_test[:int(test_size_percent*len(X_test))]
        y_test = np.array(y_test)
        y_test = y_test[:int(test_size_percent*len(y_test))]
        logger.info(f"Loaded {len(X_test)} testing samples", extra={"tag": TAG})

        return X_train, y_train, X_test, y_test

    except Exception as e:
        logger.error(f"Error in cleaning the data: {e}", extra={"tag": TAG})
        raise e