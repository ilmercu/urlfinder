from core.elements.url import URL
from urlfinder.core.finder import Finder
from core.url_parser import URLParser
from urlfinder.core.output_manager import OutputManager
import click

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--domains', '-d', help='List of comma separated scope domains')
@click.option('--check-status', '-cs', help='Get only URLs with status code between 200 and 400     [default: False]', is_flag=True, default=False)
def main(url, domains, check_status):
    scope_domains = set()  
    if domains:
        domains = domains.replace(' ', '')

        for domain in domains.split(','):
            url_parser = URLParser(url=domain, is_scope_domain=True)
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
    finder = Finder(base_url, scope_domains, output_manager, check_status)
    finder.find()

if __name__ == '__main__':
    main()
