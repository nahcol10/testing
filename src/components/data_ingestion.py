import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj_data import ProjData


class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            CustomException(e,sys)

    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info(f"Exporting data from mongodb")
            data_dto = ProjData()
            df = data_dto.export_collection_as_df(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"shape of dataframe is {df.shape}")
            feature_dir_path = os.path.dirname(self.data_ingestion_config.feature_file_path)
            os.makedirs(feature_dir_path,exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def split_data_into_train_test(self,df:DataFrame):
        try:
            train,test = train_test_split(df,test_size=self.data_ingestion_config.train_test_split_ratio)
            ingested_dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(ingested_dir_path,exist_ok=True)
            train.to_csv(self.data_ingestion_config.train_file_path)
            test.to_csv(self.data_ingestion_config.test_file_path)
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            df = self.export_data_into_feature_store()
            self.split_data_into_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(self.data_ingestion_config.train_file_path,self.data_ingestion_config.test_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
