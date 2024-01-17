import requests
import queue
import logging
from bs4 import BeautifulSoup

from .url import URL
from .output_manager import OutputManager

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s - %(message)s'
)


class Finder:
    def __init__(self, base_url: URL, all_domains: bool, output_manager: OutputManager):
        self.base_url = base_url
        self.only_same_domain = not all_domains
        self.output_manager = output_manager

        # init url queue
        self.url_queue = queue.Queue()
        self.url_queue.put(self.base_url)

        # visited urls
        self.url_set = set()

    def find(self):            
        while True:
            if self.url_queue.empty():
                break

            current_url = self.url_queue.get()
            current_url.init_base_url_alternative()
            logging.info(f'Starting visiting {current_url.get_url()}')

            # mark as visited
            self.url_set.add(current_url.get_url())
            self.url_set.add(current_url.alternative_base_url.get_url())

            try:
                response = requests.get(current_url)
            except requests.exceptions.InvalidSchema:
                print(f"Can't send request to an invalid URL. URL: {current_url}")
                continue

            bsoup = BeautifulSoup(response.text, 'html.parser')
            all_urls = bsoup.findAll('a')

            for url in all_urls:
                try:
                    new_url = URL(url.get('href'), self.base_url.get_url())
                except AttributeError as e:
                    continue
                
                new_url.init_base_url_alternative()

                if new_url.get_url() not in self.url_set and new_url.alternative_base_url.get_url() not in self.url_set:
                    if (self.only_same_domain and self.base_url.is_same_domain(new_url)):
                        logging.info(f'Found link {new_url.get_url()}')
                        logging.info(f'Add link to visit {new_url.get_url()}')
                        self.url_queue.put(new_url)
                    elif not self.only_same_domain:
                        logging.info(f'Found link {new_url.get_url()}')
                        logging.info(f'Add link to visit {new_url.get_url()}')
                        self.url_queue.put(new_url)

        logging.info(f'Writing URLs to {self.output_manager.destination_path}')

        for url in self.url_set:
            self.output_manager.write(url)
