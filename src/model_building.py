import os
import pickle
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

logs = "logs"
os.makedirs(logs,exist_ok = True)
logger = logging.getLogger()
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

logs_file_path = os.path.join(logs,"model_building")
file_handler = logging.FileHandler(logs_file_path)
file_handler.setLevel("DEBUG")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def train_model(X_train:np.ndarray,y_train:np.ndarray,params:dict) -> RandomForestRegressor:
  try:
    if len(X_train) != len(y_train):
      raise ValueError("X_train and Y_train size must be same")
    logger.info(f"initializing the paramters {params}")
    rf = RandomForestRegressor(n_estimators=params["n_estimators"])
    
    logger.info(f"model training started with {len(X_train)} number of datapoints")
    rf.fit(X_train,y_train)
    logger.info(f"Model training completed")
    return rf
  except ValueError as e:
    logger.error(f"Value error during training : {e}")
    raise
  except Exception as e:
    logger.error(f"Unexcepted error occurred during training process : {e}")
    raise
    
    
  

def save_model(model,path:str):
  try:
    os.makedirs(os.path.dirname(path),exist_ok=True)
    
    with open(path,'wb') as file:
      pickle.dump(model,file)
    logger.debug(f"Model saved to {path} successfully!!")
  except FileNotFoundError as e:
    logger.error(f"File Not Found at : {path} : {e}")
    raise
  except Exception as e:
    logger.error(f"Unexcepted error occurred while saving file : {e}")
    raise
    
      
  
def main():
  data_file = "data/featured_engineered/featured_test.csv"
  try:
    params = {
      "n_estimators": 10
    }
    df = pd.read_csv(data_file)
    logger.info("DATA file loaded successfully!!")
    X_train = df.iloc[:,:-1].values
    y_train = df.iloc[:,-1].values
    clf = train_model(X_train,y_train,params)
    model_save_path = "model/model.pth"
    logger.info(f"model saved successfully at {model_save_path}")
    save_model(clf,model_save_path)
  except FileNotFoundError as e:
    logger.error(f"File not found at {data_file} : {e}")
  except Exception as e:
    logger.error(f"Unexcepted error occured while training model : {e}")

if __name__ == '__main__':
  main()