import requests
from bs4 import BeautifulSoup

response = requests.get('https://facebook.com')

bsoup = BeautifulSoup(response.text, 'html.parser')

all_links = bsoup.findAll('a')

for link in all_links:
    print(link.get('href'))
