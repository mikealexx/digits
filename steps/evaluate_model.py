import sys
sys.path.append('../digits')
from src.logger import LoggerSingleton
logger = LoggerSingleton().get_logger()

from zenml import step
import numpy as np
from sklearn.svm import SVC

TAG = "evaluate_model.py"

@step
def evaluate_model(model: SVC, X_test: np.ndarray, y_test: np.ndarray) -> float:
    '''
    Function to evaluate the model.

    Args:
        model: Any: Model.
        X_test: np.ndarray: Testing data.
        y_test: np.ndarray: Testing labels.

    Returns:
        float: Accuracy.
    '''

    try:
        logger.info("Evaluating the model", extra={"tag": TAG})
        accuracy = model.score(X_test, y_test)
        logger.info(f"Model evaluated successfully with accuracy: {accuracy}", extra={"tag": TAG})

        return accuracy

    except Exception as e:
        logger.error(f"Error in evaluating the model: {e}", extra={"tag": TAG})
        raise e