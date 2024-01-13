import requests
import queue
from bs4 import BeautifulSoup

from lib.core.url import URL

BASE_URL = 'https://facebook.com'

ONLY_SAME_DOMAIN = True

# init url queue
url_queue = queue.Queue()
base_url = URL(BASE_URL)
url_queue.put(base_url)

# visited urls
url_set = set()


if __name__ == '__main__':
    while True:
        if url_queue.empty():
            break

        current_url = url_queue.get()
        url_set.add(current_url)

        current_url.init_base_url_alternative()

        response = requests.get(current_url)
        bsoup = BeautifulSoup(response.text, 'html.parser')
        all_urls = bsoup.findAll('a')

        for url in all_urls:
            new_url = URL(url.get('href'), BASE_URL)

            if ONLY_SAME_DOMAIN:
                if base_url.is_same_domain(new_url):
                    print(url.get('href'))
                    print(new_url)
                    print('----------')
            else:
                print(base_url)
                print(new_url)
                print('----------')

            if current_url not in url_set:
                url_queue.put(new_url)
