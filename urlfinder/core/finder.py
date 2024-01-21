import requests
import queue
import logging
from bs4 import BeautifulSoup

from .url import URL
from .output_manager import OutputManager, OutputManagerEnum

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s - %(message)s'
)


class Finder:
    def __init__(self, base_url: URL, all_domains: bool, output_manager: OutputManager):
        self.base_url = base_url
        self.only_same_domain = not all_domains
        self.output_manager = output_manager

        # URLs to visit
        self.urls_to_visit = set()
        self.urls_to_visit.add(self.base_url)

        # all URLs (visited + to visit) 
        self.all_urls = set()
        self.all_urls.add(base_url.get_url(fuzz_parameters=True))

    def find(self):            
        while True:
            if not self.urls_to_visit:
                break

            current_url = self.urls_to_visit.pop()
            current_url.init_base_url_alternative()
            logging.info(f'Starting visiting {current_url.get_url()}')
            self.output_manager.write(OutputManagerEnum.URLS_LIST_OUTPUT_FILEPATH.value, current_url.get_url())

            if current_url.is_fuzzable():
                self.output_manager.write(OutputManagerEnum.FUZZABLE_URLS_OUTPUT_FILEPATH.value, current_url.get_url(fuzz_parameters=True))

            try:
                response = requests.get(current_url)
            except requests.exceptions.InvalidSchema:
                print(f"Can't send request to an invalid URL. URL: {current_url}")
                continue

            bsoup = BeautifulSoup(response.text, 'html.parser')
            urls_list = bsoup.findAll('a')

            for url in urls_list:
                try:
                    new_url = URL(url.get('href'), self.base_url.get_url())
                except AttributeError as e:
                    continue
                
                new_url.init_base_url_alternative()

                if new_url.get_url(fuzz_parameters=True) in self.all_urls or new_url.alternative_base_url.get_url(fuzz_parameters=True) in self.all_urls:
                    continue

                if not self.only_same_domain or (self.only_same_domain and self.base_url.is_same_domain(new_url)):
                    logging.info(f'Found link -- {new_url.get_url()}')
                    logging.info(f'Add link to visit -- {new_url.get_url()}')
                    self.urls_to_visit.add(new_url)
                    self.all_urls.add(new_url.get_url(fuzz_parameters=True))
