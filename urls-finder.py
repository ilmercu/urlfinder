import requests
import queue
from bs4 import BeautifulSoup

from lib.core.url import URL

BASE_URL = 'https://facebook.com'

ONLY_SAME_DOMAIN = True

# init url queue
url_queue = queue.Queue()
url = URL(BASE_URL)
url_queue.put(url)

# visited urls
url_set = set()


if __name__ == '__main__':
    """u2 = URL(f'{BASE_URL}/')
    print(u.is_same_resource(u2))

    u3 = URL(f'{BASE_URL}/ewrcw4c')
    print(u.is_same_resource(u3))

    u4 = URL(f'{BASE_URL}?wrlwrk=2')
    print(u.is_same_resource(u4))

    u5 = URL(f'{BASE_URL}/ertrete.php?wrlwrk=2')
    print(u.is_same_resource(u5))

    u6 = URL(f'{BASE_URL}#test')
    print(u.is_same_resource(u6))"""
    
    while True:
        if url_queue.empty():
            break

        current_url = url_queue.get()
        url_set.add(current_url)

        current_url.init_base_url_alternative()
        #print(url)

        response = requests.get(current_url)
        bsoup = BeautifulSoup(response.text, 'html.parser')
        all_urls = bsoup.findAll('a')

        for url in all_urls:
            new_url = URL(url.get('href'), BASE_URL)
            print(url.get('href'))
            print(new_url)
            print('----------')
            if current_url not in url_set:
                url_queue.put(new_url)
