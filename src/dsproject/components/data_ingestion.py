import os
import sys
import pandas as pd
import mysql.connector
from dataclasses import dataclass
from src.dsproject.logger import logger
from src.dsproject.exception import CustomException

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("data", "raw", "churn.csv")
    train_data_path: str = os.path.join("data", "processed", "train.csv")
    test_data_path: str = os.path.join("data", "processed", "test.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def load_from_csv(self, file_path):
        try:
            logger.info("Reading data from CSV file")
            df = pd.read_csv(file_path)
            logger.info(f"CSV loaded successfully — shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e, sys.exc_info())

    def load_from_mysql(self, host, user, password, database, query):
        try:
            logger.info("Connecting to MySQL database")
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            logger.info("MySQL connection successful")
            df = pd.read_sql(query, connection)
            connection.close()
            logger.info(f"Data loaded from MySQL — shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e, sys.exc_info())

    def save_data(self, df):
        try:
            logger.info("Saving raw data")
            os.makedirs(os.path.dirname(
                self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logger.info(f"Raw data saved to {self.ingestion_config.raw_data_path}")
            return df
        except Exception as e:
            raise CustomException(e, sys.exc_info())


if __name__ == "__main__":
    obj = DataIngestion()
    # Load from CSV
    df = obj.load_from_csv(
        "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    obj.save_data(df)
    print(df.head())
    print(df.shape)