from urllib.parse import urlparse, parse_qsl, unquote_plus, quote_plus, ParseResult
from enum import Enum
from re import fullmatch


class URLParserEnum(Enum):
    MAIL_PROTOCOL         = 'mailto'
    MAIL_REGEX            = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    HTTP_PROTOCOL         = 'http'
    HTTPS_PROTOCOL        = 'https'

class URLParser:
    """
    URL parsing class
    """
    
    def __init__(self, url: str, base_url: str=''):
        """
        Return new URLParser instance
        
        :param url: URL to parse
        :param base_url: base url (input from the user)
        """
        
        self.url = url
        if base_url:
            self.base_url = URLParser.parse(base_url)
        self.parts = URLParser.parse(self.url)
        self.__format_url()

    @classmethod
    def parse(cls, url: str) -> ParseResult:
        """
        Parse an URL

        :param url: URL to parse
        :return: parts of URL
        """
        
        parts = urlparse(url)
        _query = parse_qsl(parts.query, keep_blank_values=True)
        _path = unquote_plus(parts.path)
        return parts._replace(query=_query, path=_path)

    def __format_url(self) -> str:
        """
        Format the URL properly

        :param url: new URL
        :base_url: original URL
        :return: formatted URL
        """

        if self.is_mail():
            return self.parts

        if '' == self.parts.scheme:
            if '' == self.base_url.scheme:
                raise AttributeError
            scheme = self.base_url.scheme
        else:
            scheme = self.parts.scheme

        if '' == self.parts.netloc:
            if '' == self.base_url.netloc:
                raise AttributeError
            netloc = self.base_url.netloc
        else:
            netloc = self.parts.netloc

        queries = ''
        for query in self.parts.query:
            query_parameter = f'{query[0]}='
            if query[1]:
                query_parameter = f'{query_parameter}{quote_plus(query[1])}'
            queries += f'{query_parameter}&'

        # removing last &
        queries = queries[:-1]

        fragment = ''
        if self.parts.fragment:
            fragment = f'#{self.parts.fragment}'

        if queries:
            return self.__reparse(f'{scheme}://{netloc}{self.parts.path}?{queries}{fragment}')
        
        return self.__reparse(f'{scheme}://{netloc}{self.parts.path}{fragment}')

    def get_parts(self) -> ParseResult:
        """
        Get parts of parsed URL

        :return: parts of URL
        """
        
        return self.parts

    def is_url(self) -> bool:
        """
        Check if the input is an URL

        :return: True if the input is a valid URL, False otherwise
        """

        if self.get_parts().scheme in [ URLParserEnum.HTTP_PROTOCOL.value, URLParserEnum.HTTPS_PROTOCOL.value ]:
            if '' != self.get_parts().netloc:
                return True
            return False
        
        return False

    def is_mail(self) -> bool:
        """
        Check if the input is a mail

        :return: True if the input is a valid mail, False otherwise
        """

        if '' != self.get_parts().scheme and URLParserEnum.MAIL_PROTOCOL.value != self.get_parts().scheme:
            return False
        
        return fullmatch(URLParserEnum.MAIL_REGEX.value, self.get_parts().path)
    
    def __reparse(self, url: str) -> ParseResult:
        """
        Set again the url and parse it
        
        :param url: changed URL
        :return: ParseResult instance containing the parts of the URL
        """
        
        self.url = url
        self.parts = URLParser.parse(url)
