from urlfinder.core.url import URL
from urlfinder.core.finder import Finder
from core.url_parser import URLParser
from core.scope_parser import ScopeParser
from urlfinder.core.output_manager import OutputManager
import click

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--domains', '-d', help='List of comma separated scope domains')
def main(url, domains):
    scope_domains = set()  
    if domains:
        domains = domains.replace(' ', '')

        for domain in domains.split(','):
            url_parser = ScopeParser(url=domain)
            new_domain = URL(url_parser.get_parts())
            scope_domains.add(new_domain)

    try:
        url_parser = URLParser(url)
        if not url_parser.is_url():
            print(f'Please provide a valid URL. Current value "{url}"')
            exit(1)
    except AttributeError as e:
        print(f'Please provide a valid URL. Current value "{url}"')
        exit(1)

    output_manager = OutputManager(url_parser.get_parts().netloc)

    base_url = URL(url_parser.get_parts())
    finder = Finder(base_url, scope_domains, output_manager)
    finder.find()

if __name__ == '__main__':
    main()
