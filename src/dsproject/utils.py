import os
import sys
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from src.dsproject.logger import logger
from src.dsproject.exception import CustomException


def save_object(file_path, obj):
    """
    Saves any Python object (model, preprocessor) to disk.
    WHY joblib over pickle?
    joblib is optimized for numpy arrays and sklearn objects —
    it's faster and more reliable for ML models specifically.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(obj, file_path)
        logger.info(f"Object saved to {file_path}")
    except Exception as e:
        raise CustomException(e, sys.exc_info())


def load_object(file_path):
    """
    Loads a saved object back from disk.
    Used in prediction pipeline to load the trained model.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found at {file_path}")
        obj = joblib.load(file_path)
        logger.info(f"Object loaded from {file_path}")
        return obj
    except Exception as e:
        raise CustomException(e, sys.exc_info())


def evaluate_models(X_train, y_train, X_test, y_test, models):
    """
    Takes a dictionary of models, trains each one, evaluates on test set.
    Returns a dictionary of results.

    WHY evaluate multiple models here instead of one?
    We don't know upfront which model works best for our data.
    So we try several and pick the best one — this is standard
    ML practice called model selection.
    """
    try:
        results = {}

        for name, model in models.items():
            logger.info(f"Training {name}")

            # train the model
            model.fit(X_train, y_train)

            # predict on test set
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            # evaluate with 3 metrics
            acc   = accuracy_score(y_test, y_pred)
            f1    = f1_score(y_test, y_pred)
            auc   = roc_auc_score(y_test, y_prob)

            results[name] = {
                "accuracy": round(acc, 4),
                "f1_score": round(f1, 4),
                "roc_auc":  round(auc, 4)
            }

            logger.info(f"{name} → Accuracy: {acc:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

        return results

    except Exception as e:
        raise CustomException(e, sys.exc_info())