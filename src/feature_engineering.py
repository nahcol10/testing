import pandas as pd
import logging
import os

logs_path = "logs"
os.makedirs(logs_path,exist_ok=True)

#creating the logging object 
logger = logging.getLogger()
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

log_file_path = os.path.join(logs_path,"feature_engineering.log")
file_handler = logging.FileHandler(log_file_path)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -%(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def feature_engineering(df:pd.DataFrame):
  return df

def main():
  try:
    train_df = pd.read_csv("data/interim/train_processed.csv")
    test_df = pd.read_csv("data/interim/test_processed.csv")
    logger.info("File Loaded successfully!!")
    
    featured_engineered_train = feature_engineering(train_df)
    featured_engineered_test = feature_engineering(test_df)
    
    to_save_path = "data/featured_engineered"
    os.makedirs(to_save_path,exist_ok=True)
    featured_engineered_train.to_csv(os.path.join(to_save_path,"featured_train.csv"),index=False)
    featured_engineered_test.to_csv(os.path.join(to_save_path,"featured_test.csv"),index=False)
    logger.info(f"Featured Data Stored successfully to :{to_save_path} ")
    logger.info("feature engineering does successfully!!")
  except FileNotFoundError as e:
    logger.error(f"Can't Find file name : {e} ")
    raise
  except Exception as e:
    logger.error(f"Unexcepted error occurred during feature engineering")


if __name__ == "__main__":
  main()

