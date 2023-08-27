import os, sys
from src.logger import logging
from src.utils import scrapper_file_path
from src.exception import CustomException
from dotenv import load_dotenv, find_dotenv
from src.scraper_script.product_scraper import WebScraper

load_dotenv(find_dotenv())

if __name__ == '__main__':
    try:
        base_url = os.environ.get('BASE_URL')
        user_agent = os.environ.get('USER_AGENT')
        headers = {'User-Agent': user_agent}

        scraper = WebScraper(base_url, user_agent, headers)
        df = scraper.run()

        logging.info(f"{df.head()}, \nData has been passed to save!")
        scrapper_file_path(df, "product_data")
        
    except Exception as e:
        logging.error(f'Error occurred : {e}')
        raise CustomException(f'Exception occurred : {e}', sys)