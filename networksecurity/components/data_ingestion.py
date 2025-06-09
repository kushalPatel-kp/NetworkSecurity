import os
import sys
import pandas as pd
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CutsomException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_enitit import DataIngestionArtifact
from typing import List
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CutsomException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_URL)
            collection=self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'], axis=1)
            df.replace({"na":np.nan}, inplace=True)

            return df
        except Exception as e:
            raise CutsomException(e,sys)
        
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
           feature_store_file_path=self.data_ingestion_config.feature_store_file_path
           dir_path=os.path.dirname(feature_store_file_path)
           os.makedirs(dir_path,exist_ok=True)
           dataframe.to_csv(feature_store_file_path,index=False,header=True)
           return dataframe
        except Exception as e:
            raise CutsomException(e,sys)
        
    def split_train_test_split(self, dataframe:pd.DataFrame):
        train_set, test_set = train_test_split(dataframe, test_size=0.2)
        logging.info("Performed Train Test Split")

        dir_name = os.path.dirname(self.data_ingestion_config.training_file_path)
        os.makedirs(dir_name,exist_ok=True)

        train_set.to_csv(
            self.data_ingestion_config.training_file_path, index=False, header=True
        )

        test_set.to_csv(
            self.data_ingestion_config.testing_file_path, index=False, header=True
        )
        
    def initate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_train_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifact


        except Exception as e:
            raise CutsomException(e,sys)

