import os, sys
from datetime import datetime
from src.logger import logging
from src.exception import CustomException

def scrapper_file_path(df, name):
    try:
        DATA_FILE=f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}_{name}.csv"
        data_path = os.path.join(os.getcwd(),'generatedData',DATA_FILE)
        os.makedirs(data_path,exist_ok=True)

        DATA_FILE_PATH = os.path.join(data_path,DATA_FILE)
        
        df.to_csv(DATA_FILE_PATH, index=False)

        logging.info("File Created Successfully at : " + DATA_FILE_PATH)
    
    except Exception as e:
        logging.error(f'Error occurred : {e}')
        raise CustomException(f'Exception occurred : {e}', sys)