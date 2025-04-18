import os
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import logging

#Ensure log director exists
log_dir='logs/'
os.makedirs(log_dir,exist_ok=True)

#Logging configuration
logger = logging.getLogger("data_ingestion")
logger.setLevel("DEBUG")

#creating the streamhandler object -> display log on console
console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

#creating the streamhandler object -> display log on files
log_file_path = os.path.join(log_dir,'data_ingestion.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel("DEBUG")

#setting the formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_data(data_url: str):
  """load data from csv file"""
  try:
    df = pd.read_csv(data_url)
    logger.info(f"data loaded from {data_url}")
    return df
  except pd.errors.ParserError as e:
    logger.error(f"Failed to parse the CSV file : {e}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error occurred while loading the data : {e}")
    raise
  
def preprocess_data(df : pd.DataFrame):
  """Preprocess the data"""
  try:
    df.columns = ['A','B','C','D']
    logger.info(f"Column name successfully to : {df.columns}")
    return df
  except KeyError as e :
    logger.error(f"Unable to rename")
    raise
  except Exception as e:
    logger.error(f"Unexpected error occurred while renaming the columns : {e}")
    raise
  
def save_data(train: pd.DataFrame,test:pd.DataFrame,save_data_url:str):
  """Save train and test data"""
  try:
    raw_data_path = os.path.join(save_data_url,"raw")
    os.makedirs(raw_data_path,exist_ok=True)
    train.to_csv(os.path.join(raw_data_path,"train.csv"),index=False)
    test.to_csv(os.path.join(raw_data_path,"test.csv"),index=False)
    logger.info(f"Train and Test save successfully to : {raw_data_path}")
  except Exception as e:
    logger.error(f"Unexpected error occur while saving data : {e}")
    raise
    
    

def main():
  try:
      test_size = 0.2
      X, _ = load_iris(return_X_y=True, as_frame=True)
      df = pd.DataFrame(X)
      final_df = preprocess_data(df)
      train, test = train_test_split(final_df, test_size=test_size, random_state=42)
      save_data(train, test, save_data_url='data/')
  except Exception as e:
      logger.error(f"Error in main: {e}")


if __name__ == '__main__':
  main()
