import os
import sys
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.dsproject.logger import logger
from src.dsproject.exception import CustomException


@dataclass
class DataIngestionConfig:
    # path configuration 
    raw_data_path: str = os.path.join("data", "raw", "churn.csv")
    train_data_path: str = os.path.join("data", "processed", "train.csv")
    test_data_path: str = os.path.join("data", "processed", "test.csv")


class DataIngestion:
    def __init__(self):
        # trigger data ingestion config on object creation 
        self.ingestion_config = DataIngestionConfig()

    def load_from_csv(self, file_path):
        try:
            logger.info("Reading data from CSV file")
            df = pd.read_csv(file_path)
            logger.info(f"CSV loaded successfully — shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e, sys.exc_info())

    def push_to_mysql(self, df, host, user, password, database):
        """
        Pushes a DataFrame into MySQL using SQLAlchemy.
        WHY SQLAlchemy and not mysql.connector directly?
        Because pandas' to_sql() method needs a SQLAlchemy engine
        to write a DataFrame — it can't use a raw connector.
        if_exists='replace' means it drops and recreates the table
        every time, so reruns are safe.
        """
        try:
            logger.info("Pushing data to MySQL via SQLAlchemy")
            engine = create_engine(
                f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            )
            df.to_sql('telco_churn', con=engine, if_exists='replace', index=False)
            logger.info(f"Data pushed to MySQL — {len(df)} rows")
        except Exception as e:
            raise CustomException(e, sys.exc_info())

    def load_from_mysql(self, host, user, password, database):
        """
        WHY read back from MySQL after we just pushed from CSV?
        Because in a real project, the database is the single source
        of truth. The CSV is just the initial seed. In production,
        new customer records would come directly from MySQL — not a file.
        So we train our pipeline to always pull from MySQL.
        """
        try:
            logger.info("Connecting to MySQL to read data")
            engine = create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            )
            query = "SELECT * FROM telco_churn"
            df = pd.read_sql(query, engine)
            logger.info(f"Data loaded from MySQL — shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(e, sys.exc_info())
        
        
    def save_raw_data(self, df):
        try:
            logger.info("Saving raw data locally")
            os.makedirs(os.path.dirname(
                self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logger.info(f"Raw data saved to {self.ingestion_config.raw_data_path}")
        except Exception as e:
            raise CustomException(e, sys.exc_info())

    def split_and_save(self, df):
        """
        WHY split here in ingestion and not in transformation?
        We split as early as possible so that the transformation
        step only ever sees training data when learning parameters
        like mean, std for scaling. This prevents data leakage —
        a very common mistake where test data accidentally influences
        how you preprocess training data, giving fake good results.
        """
        try:
            logger.info("Splitting data into train and test sets")
            train_df, test_df = train_test_split(
                df, test_size=0.2, random_state=42, stratify=df['Churn']
            )
            os.makedirs(os.path.dirname(
                self.ingestion_config.train_data_path), exist_ok=True)
            train_df.to_csv(
                self.ingestion_config.train_data_path, index=False)
            test_df.to_csv(
                self.ingestion_config.test_data_path, index=False)
            logger.info(
                f"Train shape: {train_df.shape} | Test shape: {test_df.shape}")
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e, sys.exc_info())


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    HOST = os.getenv("DB_HOST")
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE = os.getenv("DB_DATABASE")

    obj = DataIngestion()

    # Step 1: Load CSV
    df = obj.load_from_csv(
        "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

    # Step 2: Push to MySQL
    obj.push_to_mysql(df, HOST, USER, PASSWORD, DATABASE)

    # Step 3: Read back from MySQL (this is what pipeline will always use)
    df = obj.load_from_mysql(HOST, USER, PASSWORD, DATABASE)

    # Step 4: Save raw snapshot locally
    obj.save_raw_data(df)

    # Step 5: Split and save train/test
    train_path, test_path = obj.split_and_save(df)

    print(f"Train: {train_path}")
    print(f"Test:  {test_path}")
