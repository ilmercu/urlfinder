from urllib.parse import urlparse, ParseResult
from enum import Enum
from re import fullmatch, search


class URLParserEnum(Enum):
    MAIL_PROTOCOL  = 'mailto'
    MAIL_REGEX     = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    HTTP_PROTOCOL  = 'http'
    HTTPS_PROTOCOL = 'https'
    SMS_PROTOCOL   = 'sms'
    PHONE_PROTOCOL = 'tel'
    PHONE_REGEX    = r'(\+)?([^\d]*)([p\d-]+)([^\d]*)'

class URLParser:
    """
    URL parsing class
    """
    
    def __init__(self, url: str, base_url: str='', is_scope_domain: bool=False):
        """
        Return new URLParser instance
        
        :param url: URL to parse
        :param base_url: base url (input from the user)
        :param is_scope_domain: True if parsing a scope domain
        """
        
        # add protocol for scope domain
        if is_scope_domain:
            url = f'https://{url}'

        if base_url:
            self.base_url = self.parse(base_url)
        self.parts = self.parse(url)
        self.__format_url()

    def parse(self, url: str) -> ParseResult:
        """
        Parse an URL

        :param url: URL to parse
        :return: parts of URL
        """
        
        parts = urlparse(url)
        _query = self.parse_query_parameters(parts.query)

        _path = parts.path.replace(' ', '')
        if parts.scheme in [ URLParserEnum.PHONE_PROTOCOL.value, URLParserEnum.SMS_PROTOCOL.value ] and self.__is_phone_number(_path):
            _path = search(URLParserEnum.PHONE_REGEX.value, _path)
            if _path.group(1):
                _path = f'{_path.group(1)}{_path.group(3)}'
            else:
                _path = _path.group(3)
        else:
            _path = parts.path # keep the path as is, not considering the type of encoding

        return parts._replace(query=_query, path=_path)
    
    def parse_query_parameters(self, query: str) -> list:
        """
        Parse query parameters not considering the type of encoding
        
        :param query: original query string
        :return: list containing the pair (parameter_name, parameter_value)
        """
        
        if not query:
            return []

        query_parameters = query.split('&')

        result = [ ]
        for query_parameter in query_parameters:
            values = query_parameter.split('=')
            if 1 == len(values):
                value = ''
            else:
                value = values[1]
            result.append((values[0], value))

        return result

    def __is_phone_number(self, phone_number: str):
        """
        Check if a string is a phone number

        :param phone_number: phone number
        :return: True if the string is a phone number, False otherwise 
        """

        return fullmatch(URLParserEnum.PHONE_REGEX.value, phone_number) is not None

    def __format_url(self) -> str:
        """
        Format the URL properly

        :param url: new URL
        :base_url: original URL
        :return: formatted URL
        """

        if self.is_mail() or self.is_phone():
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

        path = self.parts.path
        if path.startswith('./'):
            netloc += '/'
            path = path[2:]
        elif path.startswith('../'):
            netloc += '/'

        queries = ''
        for query in self.parts.query:
            query_parameter = f'{query[0]}='
            if query[1]:
                query_parameter = f'{query_parameter}{query[1]}'
            queries += f'{query_parameter}&'

        # removing last &
        queries = queries[:-1]

        fragment = ''
        if self.parts.fragment:
            fragment = f'#{self.parts.fragment}'

        if queries:
            return self.__reparse(f'{scheme}://{netloc}{path}?{queries}{fragment}')
        
        return self.__reparse(f'{scheme}://{netloc}{path}{fragment}')

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

    def is_phone(self) -> bool:
        """
        Check if the URL is a phone number

        :return: True if the input is a valid phone number, False otherwise
        """

        parts = self.get_parts()
        if '' == parts.scheme or parts.scheme not in [ URLParserEnum.PHONE_PROTOCOL.value, URLParserEnum.SMS_PROTOCOL.value ]:
            return False
        
        return self.__is_phone_number(self.get_parts().path)
    
    def __reparse(self, url: str) -> ParseResult:
        """
        Set again the url and parse it
        
        :param url: changed URL
        :return: ParseResult instance containing the parts of the URL
        """
        
        self.parts = self.parse(url)
