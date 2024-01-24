import requests
import queue
import logging
from bs4 import BeautifulSoup

from .url import URL
from .mail import Mail
from .url_parser import URLParser
from .output_manager import OutputManager, OutputManagerEnum

logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s - %(message)s'
)


class Finder:
    def __init__(self, base_url: URL, all_domains: bool, output_manager: OutputManager):
        """
        Return new Finder instance
        :parameter base_url: URL object representing the base URL (user input)
        :parameter all_domains: bool representing if the tool must retrieve URLs coming from an infinite set of domains
        :parameter output_manager: OutputManager instance which handles output files
        """
        
        self.base_url = base_url
        self.only_same_domain = not all_domains
        self.output_manager = output_manager

        # URLs to visit
        self.urls_to_visit = set()
        self.urls_to_visit.add(self.base_url)

        # all URLs (visited + to visit) 
        self.all_urls = set()
        self.all_urls.add(base_url.get_url(fuzz_parameters=True))

        # mail set
        self.mails = set()

    def find(self):
        """
        Retrieve URLs and save them in output files
        """
        
        while True:
            if not self.urls_to_visit:
                break

            current_url = self.urls_to_visit.pop()
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
                if not url.get('href'): # skip empty value
                    continue

                url_parser = URLParser(url.get('href'), self.base_url.get_url())

                if url_parser.is_mail():
                    mail = Mail(url_parser.get_parts())
                    if mail not in self.mails:
                        self.mails.add(mail)
                        self.output_manager.write(OutputManagerEnum.MAIL_OUTPUT_FILEPATH.value, mail.get_mail())
                    continue

                try:
                    new_url = URL(url_parser.get_parts(), self.base_url.get_url())
                except AttributeError as e:
                    continue
                
                if new_url.get_url(fuzz_parameters=True) in self.all_urls:
                    continue

                if not self.only_same_domain or (self.only_same_domain and self.base_url.is_same_domain(new_url)):
                    logging.info(f'Found link -- {new_url.get_url()}')
                    logging.info(f'Add link to visit -- {new_url.get_url()}')
                    self.urls_to_visit.add(new_url)

                    # add fuzzed parameters in order to avoid duplications due to only parameter's values (e.g http://abc.com?test=1 and http://abc.com?test=2)
                    self.all_urls.add(new_url.get_url(fuzz_parameters=True))
