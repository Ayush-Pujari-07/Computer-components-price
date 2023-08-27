import os, sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from src.logger import logging
from src.exception import CustomException
from src.utils import scrapper_file_path
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class WebScraper:
    def __init__(self, base_url, user_agent, headers=None):
        self.base_url = base_url
        self.user_agent = user_agent
        self.headers = headers
        self.pcComponents_url_list = []
        self.product_data = []
        self.product_url_list = []
        self.product_name_list = []
        self.product_rating_list = []
        self.product_price_list = []
        self.product_in_stock_list = []
        self.product_scraped_date_time = []

    def _get_soup(self, url):
        page = requests.get(url, headers=self.headers)
        return BeautifulSoup(page.content, 'html.parser')
    
    def _scrape_product_data(self, link):
        try:
            time.sleep(0.5)
            product_page = requests.get(link, headers=self.headers)
            product_soup = BeautifulSoup(product_page.content, 'html.parser')
            # this is to get the product details for products with multiple pages.
            if product_soup.find('div',{"class":"wd-loop-footer products-footer"}):
                pages = product_soup.find('div',{"class":"wd-loop-footer products-footer"}).find('ul',{"class":"page-numbers"}).find_all('li')[-2].text
                logging.info(f"The link is : {link}, and no of pages are : {pages}")
                for page in range(1, int(pages)+1):
                    time.sleep(1)
                    inner_page_url = f"{link}page/{page}/"
                    logging.info(inner_page_url)
                    inner_page = requests.get(inner_page_url, headers=self.headers)
                    inner_soup = BeautifulSoup(inner_page.content, 'html.parser')
                    inner_products_blocks = inner_soup.find_all('div',{"class":"product-wrapper"})
                    for product in inner_products_blocks:
                        product_url = product.find('div',{"class":"product-element-bottom"}).find('h3').find('a')['href']
                        if product_url:
                            self.product_url_list.append(product_url)
                        else:
                            self.product_url_list.append('Not Found')
                        product_name = product.find('div',{"class":"product-element-bottom"}).find('h3').text
                        if product_name:
                            self.product_name_list.append(product_name)
                        else:
                            self.product_name_list.append('Not Found')
                        product_rating = product.find('div',{"class":"product-element-bottom"}).find('div',{"class":"wd-star-rating"}).text.strip().split(' ')[1]
                        if product_rating:
                            self.product_rating_list.append(product_rating)
                        else:
                            self.product_rating_list.append('Not Found')
                        product_price = product.find('div',{"class":"product-element-bottom"}).find('div',{"class":"wrap-price"}).text.strip()
                        if product_price:
                            self.product_price_list.append(product_price)
                        else:
                            self.product_price_list.append('Not Found')
                        product_in_stock = product.find('div',{"class":"product-element-bottom"}).find('p').text.strip()
                        if product_in_stock:
                            self.product_in_stock_list.append(product_in_stock)
                        else:
                            self.product_in_stock_list.append('Not Found')
                        self.product_scraped_date_time.append(datetime.now().strftime('%d/%m/%Y-%H:%M'))

            # this is to get the product details for products with one page.
            else:
                time.sleep(1)
                logging.info(f"The link is : {link}, and no of pages are : 0")
                inner_page = requests.get(link, headers=self.headers)
                inner_soup = BeautifulSoup(inner_page.content, 'html.parser')
                inner_products_blocks = inner_soup.find_all('div',{"class":"product-wrapper"})

                for product in inner_products_blocks:
                    product_url = product.find('div',{"class":"product-element-bottom"}).find('h3').find('a')['href']
                    if product_url:
                        self.product_url_list.append(product_url)
                    else:
                        self.product_url_list.append('Not Found')
                    product_name = product.find('div',{"class":"product-element-bottom"}).find('h3').text
                    if product_name:
                        self.product_name_list.append(product_name)
                    else:
                        self.product_name_list.append('Not Found')
                    product_rating = product.find('div',{"class":"product-element-bottom"}).find('div',{"class":"wd-star-rating"}).text.strip().split(' ')[1]
                    if product_rating:
                        self.product_rating_list.append(product_rating)
                    else:
                        self.product_rating_list.append('Not Found')
                    product_price = product.find('div',{"class":"product-element-bottom"}).find('div',{"class":"wrap-price"}).text.strip()
                    if product_price:
                        self.product_price_list.append(product_price)
                    else:
                        self.product_price_list.append('Not Found')
                    product_in_stock = product.find('div',{"class":"product-element-bottom"}).find('p').text.strip()
                    if product_in_stock:
                        self.product_in_stock_list.append(product_in_stock)
                    else:
                        self.product_in_stock_list.append('Not Found')
                    self.product_scraped_date_time.append(datetime.now().strftime('%d/%m/%Y-%H:%M'))
        except Exception as e:
            logging.error(f'Error occurred : {e}')
            raise CustomException(f'Exception occurred : {e}', sys)

    def scrape(self):
        try:
            logging.info("Scraping Started")
            soup = self._get_soup(self.base_url)
            for href in soup.find_all('a', href=True):
                if "https://modxcomputers.com/product-category/pc-components/" in href['href']:
                    url = urljoin(self.base_url, href['href'])
                    if len(urlparse(url).path.split('/')) <= 5:
                        self.pcComponents_url_list.append(href['href'])

            self.pcComponents_url_list = list(dict.fromkeys(self.pcComponents_url_list))
            
            logging.info(f"Product Url list : {self.pcComponents_url_list}")
            
            for link in self.pcComponents_url_list:
                self._scrape_product_data(link)

            self.product_data = {
                    'product_scraped_date_time' : self.product_scraped_date_time,
                    'product_name' : self.product_name_list,
                    'product_rating_of_5' : self.product_rating_list,
                    'product_price' : self.product_price_list,
                    'product_in_stock' : self.product_in_stock_list,
                    'product_url' : self.product_url_list
            }
            logging.info(f"Scraping Completed {self.product_data}")

        except Exception as e:
            logging.error(f'Error occurred : {e}')
            raise CustomException(f'Exception occurred : {e}', sys)
    def _to_dataFrame(self):
        df = pd.DataFrame(self.product_data)
        return df

    def run(self):
        self.scrape()
        df = self._to_dataFrame()
        return df

# if __name__=="__main__":
#     try:
#         base_url = os.environ.get('BASE_URL')
#         user_agent = os.environ.get('USER_AGENT')
#         headers = {'User-Agent': user_agent}

#         scraper = WebScraper(base_url, user_agent, headers)
#         df = scraper.run()

#         logging.info(f"{df.head()}, \nData has been passed to save!")
#         scrapper_file_path(df, "product_data")
        
#     except Exception as e:
#         logging.error(f'Error occurred : {e}')
#         raise CustomException(f'Exception occurred : {e}', sys)