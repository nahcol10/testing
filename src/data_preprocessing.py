import os
import pandas as pd
import logging


logs_path = "logs"
os.makedirs(logs_path, exist_ok=True)

logger = logging.getLogger()
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

log_file_path = os.path.join(logs_path, 'data_preprocessing.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel("DEBUG")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def preprocess_df(data: pd.DataFrame):
    return data

def main():
    try:
        # load dataset
        train_df = pd.read_csv("data/raw/train.csv")
        test_df = pd.read_csv("data/raw/test.csv")
        logger.debug("DATA loaded successfully!!")

        train_process_df = pd.DataFrame(preprocess_df(train_df))
        test_process_df = pd.DataFrame(preprocess_df(test_df))

        data_path = "data/interim"
        os.makedirs(data_path, exist_ok=True)
        train_process_df.to_csv(os.path.join(data_path, 'train_processed.csv'), index=False)
        test_process_df.to_csv(os.path.join(data_path, 'test_processed.csv'), index=False)
        logger.debug("Processed data saved successfully to %s", data_path)
    except FileNotFoundError as e:
        logger.error(f"File not found : {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"No data : {e}")
    except Exception as e:
        logger.error(f"Failed to complete the data transformation process: {e}")

if __name__ == '__main__':
    main()