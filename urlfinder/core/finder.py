import requests
from bs4 import BeautifulSoup
from enum import Enum
import logging
from urllib3.exceptions import ReadTimeoutError

from .elements.url import URL
from .elements.base_element import BaseElement
from .url_parser import URLParser
from .output_manager import OutputManager, OutputManagerEnum


class FinderColorEnum(Enum):
    SUCCESS_GREEN = '\033[92m'
    ERROR_RED     = '\033[91m'
    END_COLOR     = '\033[0m'


class Finder:
    def __init__(self, base_url: URL, scope_domains: set, output_manager: OutputManager, check_status: bool):
        """
        Return new Finder instance

        :param base_url: URL object representing the base URL (user input)
        :param scope_domains: domains in scope
        :param output_manager: OutputManager instance which handles output files
        :param check_status: get only URLs with status code in [200, 400)
        """
        
        logging.basicConfig(filename=f'{output_manager.base_path}{OutputManagerEnum.LOG_OUTPUT_FILENAME.value}', format='%(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=logging.INFO)
        self.logger = logging.getLogger(f'{output_manager.base_path}{OutputManagerEnum.LOG_OUTPUT_FILENAME.value}')

        self.base_url = base_url
        self.scope_domains = scope_domains
        self.output_manager = output_manager
        self.check_status = check_status

        # URLs to visit
        self.urls_to_visit = set()
        self.urls_to_visit.add(self.base_url)

        # all URLs (visited + to visit) 
        self.all_urls = set()
        self.all_urls.add(base_url.get_value(fuzz_parameters=True))

        # mail set
        self.mails = set()

        # phone set
        self.phones = set()

    def find(self):
        """
        Retrieve URLs and save them in output files
        """
        
        while True:
            if not self.urls_to_visit:
                break

            current_url = self.urls_to_visit.pop()
            self.logger.info(f'Scanning {current_url}')

            if (not self.scope_domains and self.base_url.is_same_domain(current_url)) or \
            current_url.is_in_scope(self.scope_domains):
                self.output_manager.write(OutputManagerEnum.URLS_LIST_OUTPUT_FILENAME, current_url.get_value())

                if current_url.is_fuzzable():
                    self.output_manager.write(OutputManagerEnum.FUZZABLE_URLS_OUTPUT_FILENAME, current_url.get_value(fuzz_parameters=True))

            try:
                response = requests.get(current_url)

                if self.check_status and not response.ok:
                    self.logger.warning(f'{current_url} status code: {response.status_code}')
                    print(f'{FinderColorEnum.ERROR_RED.value}{current_url}{FinderColorEnum.END_COLOR.value}')
                    continue
            except requests.exceptions.InvalidSchema:
                self.logger.error(f"Can't send request to an invalid URL. URL: {current_url}")
                print(f'{FinderColorEnum.ERROR_RED.value}{current_url}{FinderColorEnum.END_COLOR.value}')
                continue
            except requests.exceptions.ConnectionError:
                self.logger.error(f'Failed to resolve {current_url}')
                print(f'{FinderColorEnum.ERROR_RED.value}{current_url}{FinderColorEnum.END_COLOR.value}')
                continue
            except ReadTimeoutError:
                self.logger.error(f'Can\'t get a response from {current_url}')
                print(f'{FinderColorEnum.ERROR_RED.value}{current_url}{FinderColorEnum.END_COLOR.value}')
                continue

            print(f'{FinderColorEnum.SUCCESS_GREEN.value}{current_url}{FinderColorEnum.END_COLOR.value}')

            bsoup = BeautifulSoup(response.text, 'html.parser')
            self.__search_tags_a(bsoup, current_url)
            self.__search_tags_form(bsoup, current_url)

    def __update_urls_set(self, url_parser: URLParser):
        """
        Update the set of URLs adding a new parsed URL

        :param url_parser: parser containing the parts of the URL 
        """
        
        try:
            new_url = URL(url_parser.get_parts())
        except AttributeError as e:
            return

        if new_url.get_value(fuzz_parameters=True) in self.all_urls:
            return

        # if no scope domains were specified and the URL is in base domain or the domain is in scope
        if (not self.scope_domains and self.base_url.is_same_domain(new_url)) or \
            new_url.is_in_scope(self.scope_domains):
            self.urls_to_visit.add(new_url)

            # add fuzzed parameters in order to avoid duplications due to only parameter's values (e.g http://abc.com?test=1 and http://abc.com?test=2)
            self.all_urls.add(new_url.get_value(fuzz_parameters=True))
    
    def __search_tags_a(self, bsoup: BeautifulSoup, current_base_url: URL):
        """
        Retrieve action URL from a tags
        
        :param bsoup: BeautifulSoup instance containing the content of the page
        :param current_base_url: current URL which will be used as the base URL or its children
        """

        urls_list = bsoup.findAll('a')

        for url in urls_list:
            if not url.get('href'): # skip empty value
                continue

            self.logger.info(f'Found a href value: {url.get("href")}')

            url_parser = URLParser(url.get('href'), current_base_url.get_value())

            if url_parser.is_mail():
                mail = BaseElement(url_parser.get_parts())
                if mail not in self.mails:
                    self.mails.add(mail)
                    self.output_manager.write(OutputManagerEnum.MAIL_OUTPUT_FILENAME, mail.get_value())
                continue

            if url_parser.is_phone():
                phone = BaseElement(url_parser.get_parts())
                if phone not in self.phones:
                    self.phones.add(phone)
                    self.output_manager.write(OutputManagerEnum.PHONE_OUTPUT_FILENAME, phone.get_value())
                continue

            self.__update_urls_set(url_parser)
    
    def __search_tags_form(self, bsoup: BeautifulSoup, current_base_url: URL):
        """
        Retrieve action URL from form tags
        
        :param bsoup: BeautifulSoup instance containing the content of the page
        :param current_base_url: current URL which will be used as the base URL or its children
        """
        
        forms_list = bsoup.findAll('form')

        for form in forms_list:
            if not form.get('action'): # skip empty value
                continue

            self.logger.info(f'Found form action value: {form.get("action")}')

            url_parser = URLParser(form.get('action'), current_base_url.get_value())
            self.__update_urls_set(url_parser)
