import os
import pymongo
import sys
import certifi

from src.exception import CustomException
from src.logger import logging
from src.constants import MONGODB_URL,DATABASE_NAME

ca = certifi.where()
class MongoDBClient:
    client = None

    def __init__(self , database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongodb_url = os.getenv(MONGODB_URL)
                if mongodb_url is None:
                    raise CustomException(f"MONGODB_URL is not set for {DATABASE_NAME}")
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongodb_url,tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = MongoDBClient.client[database_name]
            self.database_name = self.database
            logging.info("MONGODB Connected successfully")

        except Exception as e:
            raise CustomException(e,sys)


