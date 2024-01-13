from lib.core.url import URL
from lib.core.finder import Finder
import click

#BASE_URL = 'https://facebook.com'
#ONLY_SAME_DOMAIN = True

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--all-domain', '-ad', help='Scan all domains   [default: False]', is_flag=True, show_default=True, default=False)
def main(url, all_domain):
    base_url = URL(url)
    finder = Finder(base_url, all_domain)
    finder.find()

if __name__ == '__main__':
    main()
