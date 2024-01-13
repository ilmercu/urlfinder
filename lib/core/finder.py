import requests
import queue
from bs4 import BeautifulSoup

from .url import URL


class Finder:
    def __init__(self, base_url: URL, all_domains: bool):
        self.base_url = base_url
        self.only_same_domain = not all_domains

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
            self.url_set.add(current_url)

            current_url.init_base_url_alternative()

            try:
                response = requests.get(current_url)
            except requests.exceptions.InvalidSchema:
                print(f"Can't send request to an invalid URL. URL: {current_url}")
                continue

            bsoup = BeautifulSoup(response.text, 'html.parser')
            all_urls = bsoup.findAll('a')

            for url in all_urls:
                new_url = URL(url.get('href'), self.base_url.human_readable_url())

                if self.only_same_domain:
                    if self.base_url.is_same_domain(new_url):
                        print(url.get('href'))
                        print(new_url)
                        print('----------')
                else:
                    print(self.base_url)
                    print(new_url)
                    print('----------')

                if current_url not in self.url_set:
                    self.url_queue.put(new_url)
