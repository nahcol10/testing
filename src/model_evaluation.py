import os
import pandas as pd
import numpy as np
import logging
from sklearn.metrics import r2_score,root_mean_squared_error
import pickle
import json

logs = "logs"
os.makedirs(logs,exist_ok=True)
logger = logging.getLogger()
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

log_path = os.path.join(logs,"model_evaluation.log")
file_handler = logging.FileHandler(log_path)
file_handler.setLevel("DEBUG")


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_model(model_path:str):
  try:
    
    with open(model_path,"rb") as file:
      model = pickle.load(file)
    logger.info(f"Model loaded from {model_path}")
    return model
  except FileNotFoundError:
    logger.error(f"File not found at : {model_path}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error occured while loading model from {model_path} :  {e}")
    raise

def load_data(data_path:str) -> pd.DataFrame:
  try:
    df = pd.read_csv(data_path)
    logger.info(f"data loaded from {data_path}")
    return df
  except FileNotFoundError:
    logger.error(f"data file not found at {data_path}")
    raise
  except Exception as e:
    logger.error(f"Unexcepted error occurred while loading the file : {e}")
    raise

def evaluate_model(model,X_test:np.ndarray , y_test:np.ndarray) -> dict:
  try:
    if len(X_test) != len(y_test):
      raise ValueError(f"X_test and y_test size must be same : {len(X_test)}")
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    rmse = root_mean_squared_error(y_test,y_pred)
    
    metrics = {
      "r2_score": r2,
      "rmse": rmse
    }
    
    logger.info("model evalution metrics calcuated")
    return metrics
  except Exception as e:
    logger.error(f"Unexcepted error occurred during model evaluation : {e}")
    raise
  
def save_metrics(metrics:dict,file_path:str):
  try:
    if dict == None:
      raise ValueError(f"Unexpected value of metics: {metrics}")
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    with open(file_path,"w") as file:
      json.dump(metrics,file,indent=4)
    logger.info(f"metric saved successfully at {file_path}")
  except Exception as e:
    logger.error(f"Error occurred while saving metrics : {e}")
    raise
      
def main():
  model = load_model("model/model.pth")
  test_data = load_data("data/featured_engineered/featured_test.csv")
  
  X_test = test_data.iloc[:,:-1].values
  y_test = test_data.iloc[:,-1].values
  
  metrics = evaluate_model(model,X_test,y_test)
  save_metrics(metrics,"model/metrics.json")

if __name__ == '__main__':
  main()
