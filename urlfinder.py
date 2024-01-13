from lib.core.url import URL
from lib.core.finder import Finder

BASE_URL = 'https://facebook.com'

ONLY_SAME_DOMAIN = True

if __name__ == '__main__':
    base_url = URL(BASE_URL)
    finder = Finder(base_url, ONLY_SAME_DOMAIN)
    finder.find()
