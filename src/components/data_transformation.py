import sys
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from src.constants import *
from src.logger import logging
from src.exception import CustomException
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.utils.main_utils import read_yaml_file, save_object, save_numpy_array_data


class DataTransformation:

    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_transformation_config:DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path:str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except:
            raise ValueError(f"{file_path} doesn't find")

    def get_data_transformation_obj(self) -> Pipeline:
        try:
            st_scaler = StandardScaler()
            mm_scaler = MinMaxScaler()

            st_feature = self._schema_config["num_features"]
            mm_feature = self._schema_config["mm_columns"]

            trf1 = ColumnTransformer(
                transformers=[
                    ("standard_scaler",st_scaler,st_feature),
                    ("min_max_scaling",mm_scaler,mm_feature)
                ],
                remainder='passthrough'
            )

            pipeline = Pipeline(steps=[
                ("scaling",trf1)
            ])

            return pipeline

        except Exception as e:
            raise CustomException(e,sys)

    def _map_gender_column(self, df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logging.info("Mapping 'Gender' column to binary values")
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df

    def _create_dummy_columns(self,df):
        df = pd.get_dummies(df,drop_first=True)
        return df


    def _rename_columns(self, df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting to int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df

    def _drop_id_column(self, df):
        """Drop the 'id' column if it exists."""
        logging.info("Dropping 'id' column")
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis=1)
        return df

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation component for the pipeline.
        """
        try:
            logging.info("Data Transformation Started !!!")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)

            # Load train and test data
            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Train-Test data loaded")

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info("Input and Target cols defined for both train and test df.")

            # Apply custom transformations in specified sequence
            input_feature_train_df = self._map_gender_column(input_feature_train_df)
            input_feature_train_df = self._drop_id_column(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columns(input_feature_train_df)

            input_feature_test_df = self._map_gender_column(input_feature_test_df)
            input_feature_test_df = self._drop_id_column(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columns(input_feature_test_df)
            logging.info("Custom transformations applied to train and test data")

            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformation_obj()
            logging.info("Got the preprocessor object")

            logging.info("Initializing transformation for Training-data")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            logging.info("Initializing transformation for Testing-data")
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Transformation done end to end to train-test df.")

            logging.info("Applying SMOTEENN for handling imbalanced dataset.")
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )
            logging.info("SMOTEENN applied to train-test df.")

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logging.info("feature-target concatenation done for train-test df.")

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info("Saving transformation object and transformed files.")

            logging.info("Data transformation completed successfully")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise CustomException(e, sys) from e

