import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

from zenml import step
import numpy as np
from sklearn.svm import SVC
from typing import Any

TAG = "train_model.py"

@step
def train_model(X_train: np.ndarray, y_train: np.ndarray) -> SVC:
    '''
    Function to train the model.

    Args:
        X_train: np.ndarray: Training data.
        y_train: np.ndarray: Training labels.

    Returns:
        Any: Model.
    '''

    try:
        logger.info("Training the model", extra={"tag": TAG})
        model = SVC()
        model.fit(X_train, y_train)
        logger.info("Model trained successfully", extra={"tag": TAG})

        return model

    except Exception as e:
        logger.error(f"Error in training the model: {e}", extra={"tag": TAG})
        raise e