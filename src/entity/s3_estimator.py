from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import CustomException
from src.entity.estimator import MyModel
import sys
from pandas import DataFrame
from typing import Optional


class S3Estimator:
    """
    This class is used to save and retrieve our model from s3 bucket and to do prediction
    """

    def __init__(self,bucket_name,model_path,):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: Optional[MyModel] = None


    def is_model_present(self):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=self.model_path)
        except CustomException as e:
            print(e)
            return False

    def load_model(self,) -> MyModel:
        """
        Load the model from the model_path
        :return:
        """
        model = self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
        if not isinstance(model, MyModel):
            raise CustomException(Exception(f"Loaded object is not of type MyModel: {type(model)}"), sys)
        return model

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to the model_path
        :param from_file: Your local system model path
        :param remove: By default it is false that mean you will have your model locally available in your system folder
        :return:
        """
        try:
            self.s3.upload_file(from_file,
                                to_filename=self.model_path,
                                bucket_name=self.bucket_name,
                                remove=remove
                                )
        except Exception as e:
            raise CustomException(e, sys)


    def predict(self, dataframe: DataFrame):
        """
        :param dataframe:
        :return:
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            # Ensure loaded_model is not None before prediction, although load_model should handle this.
            if self.loaded_model is None:
                 raise CustomException(Exception("Model could not be loaded for prediction."), sys)
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            # Raise the original exception if it's already a CustomException
            if isinstance(e, CustomException):
                raise e
            # Otherwise, wrap it in a CustomException
            raise CustomException(e, sys)