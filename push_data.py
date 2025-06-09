import sys
import json
import os
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import CutsomException

load_dotenv()

MONG_DB_URL=os.getenv("MONGO_DB_URL")
print(MONG_DB_URL)

ca=certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CutsomException(e,sys)
        
    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records=data.to_dict(orient='records')

            return records

        except Exception as e:
            raise CutsomException(e,sys)
        
    def insert_data_mongo(self,records,database,collection):
        try:
            self.database= database
            self.collection=collection
            self.records=records

            self.mongo_clint=pymongo.MongoClient(MONG_DB_URL)
            self.database = self.mongo_clint[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise CutsomException(e,sys)

if __name__ == "__main__":
    FILE_PATH=r"D:\ML_Proj\Network_Data\phisingData.csv"
    database="KushalAI"
    collection="NetworkData"
    network_obj=NetworkDataExtract()
    records=network_obj.cv_to_json_converter(file_path=FILE_PATH)
    no_of_record=network_obj.insert_data_mongo(records=records, database=database,collection=collection)
    print(no_of_record)