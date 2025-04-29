import numpy as np
import pandas as pd
import sys
from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import CustomException
from src.logger import logging
from src.constants import DATABASE_NAME,COLLECTION_NAME


class ProjData:

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e,sys)

    def export_collection_as_df(self, collection_name:str = COLLECTION_NAME , database_name:str = DATABASE_NAME ) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.database_name[collection_name]

            # Convert collection data to DataFrame and preprocess
            print("Fetching data from mongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fecthed with len: {len(df)}")
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise CustomException(e,sys)


