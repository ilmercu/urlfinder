from urlfinder.core.url import URL
from urlfinder.core.finder import Finder
from urlfinder.core.output_manager import OutputManager
import click

@click.command()
@click.option('--url', '-u', help='URL', required=True)
@click.option('--output-path', '-o', help='Output file path. If not specified output only on terminal')
@click.option('--all-domain', '-a', help='Scan all domains   [default: False]', is_flag=True, show_default=True, default=False)
def main(url, output_path, all_domain):
    output_manager = OutputManager(output_path) if output_path else None
    base_url = URL(url)
    finder = Finder(base_url, all_domain, output_manager)
    finder.find()

if __name__ == '__main__':
    main()
