import json
import os
import sys
from pandas import DataFrame,read_csv
from src.logger import logging
from src.exception import CustomException
from src.constants import *
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.utils.main_utils import read_yaml_file



class DataValidation:
    def __init__(self,data_ingestion_artifacts: DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self, df: DataFrame ) -> bool :
        try:
            status = len(df.columns) == len(self._schema_config["columns"])
            logging.info(f"is required columns present : {status}")
            return status
        except Exception as e:
            raise CustomException(e,sys)

    def is_column_exists(self,df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                 logging.info(f"missing numerical columns : {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                 logging.info(f"missing categorical columns : {missing_categorical_columns}")

            return False if len(missing_numerical_columns) > 0 | len(missing_categorical_columns) > 0 else True

        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path:str) -> DataFrame:
        try:
            return read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def initialize_data_validation(self) -> DataValidationArtifact:
        try:
            validation_error_message = ""
            train , test = (DataValidation.read_data(self.data_ingestion_artifacts.trained_file_path),DataValidation.read_data(self.data_ingestion_artifacts.test_file_path))
            train_status  = self.is_column_exists(train)
            if not train_status:
                validation_error_message += "Columns are missing in training dataframe"
            test_status = self.is_column_exists(test)
            if not test_status:
                validation_error_message += "Columns are missing in Testing dataframe"

            data_validation_artifact = DataValidationArtifact(
                validation_status=(train_status and test_status),
                message = validation_error_message,
                validation_report_file_path=self.data_validation_config.data_validation_report_file_path
            )

            report_dir = os.path.dirname(self.data_validation_config.data_validation_report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            validation_report = {
                "validation_status" : (train_status and test_status),
                "message": validation_error_message.strip()
            }

            with open(self.data_validation_config.data_validation_report_file_path,"w") as report_path:
                json.dump(validation_report,report_path,indent=4)

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)
