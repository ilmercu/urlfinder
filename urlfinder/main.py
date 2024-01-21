from urlfinder.core.url import URL
from urlfinder.core.finder import Finder
from urlfinder.core.output_manager import OutputManager
import click

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--all-domain', '-a', help='Scan all domains   [default: False]', is_flag=True, show_default=True, default=False)
def main(url, all_domain):
    output_manager = OutputManager()
    base_url = URL(url)
    finder = Finder(base_url, all_domain, output_manager)
    finder.find()

if __name__ == '__main__':
    main()
