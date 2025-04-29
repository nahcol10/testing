# from src.configuration.mongo_db_connection import MongoDBClient
# MongoDBClient()

# from src.data_access.proj_data import ProjData
# from src.constants import COLLECTION_NAME
# proj = ProjData()
# proj.export_collection_as_df(COLLECTION_NAME)
#
# from src.components.data_ingestion import DataIngestion
#
# di = DataIngestion()
# di.initiate_data_ingestion()

from src.pipline.training_pipeline import TrainPipeline

pipline = TrainPipeline()
pipline.run_pipeline()