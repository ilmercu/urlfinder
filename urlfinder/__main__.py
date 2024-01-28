from urlfinder.core.url import URL
from urlfinder.core.finder import Finder
from urlfinder.core.url_parser import URLParser
from urlfinder.core.output_manager import OutputManager
import click

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--all-domain', '-a', help='Scan all domains   [default: False]', is_flag=True, show_default=True, default=False)
def main(url, all_domain):    
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
    finder = Finder(base_url, all_domain, output_manager)
    finder.find()

if __name__ == '__main__':
    main()
