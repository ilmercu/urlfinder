from urllib.parse import urlparse, parse_qsl, unquote_plus, quote_plus, ParseResult

class ScopeParser:
    """
    Scope domain parsing class
    """
    
    def __init__(self, url: str):
        self.url = f'https://{url}'
        self.parts = self.parse()

    def parse(self) -> ParseResult:
        """
        Parse an URL

        :return: parts of URL
        """
        
        parts = urlparse(self.url)
        _query = parse_qsl(parts.query, keep_blank_values=True)
        _path = unquote_plus(parts.path)
        return parts._replace(query=_query, path=_path)

    def get_parts(self) -> ParseResult:
        """
        Get parts of parsed URL

        :return: parts of URL
        """
        
        return self.parts
