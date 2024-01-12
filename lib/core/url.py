from __future__ import annotations
from urllib.parse import urlparse, parse_qsl, unquote_plus, quote_plus
    
class URL:
    def __init__(self, url: str, base_url: str=''):
        if base_url:
            url = self.__format_url(url, base_url)

        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)
    
    def __str__(self):
        if self.parts.query:
            queries = ''

            for query in self.parts.query:
                queries += f'{query[0]}={quote_plus(query[1])}&'

            # removing last &
            queries = queries[:-1]
            
            return f'{self.parts.scheme}://{self.parts.netloc}{self.parts.path}?{queries}{self.parts.fragment}'

        return f'{self.parts.scheme}://{self.parts.netloc}{self.parts.path}{self.parts.fragment}'

    def init_base_url_alternative(self):
        if '/' == self.parts.path:
            self.alternative_base_url = URL(f'{self.parts.scheme}://{self.parts.netloc}')
        else:
            self.alternative_base_url = URL(f'{self.parts.scheme}://{self.parts.netloc}{self.parts.params}')

    def __format_url(self, url: str, base_url: str):
        if '#' == url:
            return base_url
        
        if url.startswith('/'):
            return f'{base_url}{url}'
        
        return f'{base_url}/{url}'
    
    def is_same_resource(self, second_url: URL):
        """
        Check if two URLs are the same
        :param second_url: second URL
        :return: True if two resources are the same, False otherwise
        """

        # test if objects are the same
        if second_url == self or second_url == self.alternative_base_url:
            return True

        # test if domains are the same 
        if second_url.parts.netloc == self.alternative_base_url.parts.netloc:
            # test if paths are the same 
            if second_url.parts.path == self.alternative_base_url.parts.path:
                return True
        
            # test if the only difference is the final slash
            if ('/' == second_url.parts.path and '' == self.parts.path) or ('/' == self.parts.path and '' == second_url.parts.path):
                return True
        
        return False