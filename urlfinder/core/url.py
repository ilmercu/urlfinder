from __future__ import annotations
from urllib.parse import urlparse, parse_qsl, unquote_plus, quote_plus
from tldextract import extract as domain_extractor


class URL:
    def __init__(self, url: str, base_url: str=''):
        """
        Return new URL instance
        :param url: new URL
        :param base_url: original URL (needed only if not creating original URL instance)
        """
        
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
        return self.get_url()

    def get_url(self, fuzz: bool=False):
        if self.parts.query:
            queries = ''

            # compose query
            i = 0
            for query in self.parts.query:
                if fuzz:
                   queries += f'{query[0]}=FUZZ{i}'
                else:
                    queries += f'{quote_plus(query[1])}&'
                i += 1

            # removing last &
            queries = queries[:-1]
            
            return f'{self.parts.scheme}://{self.parts.netloc}{self.parts.path}?{queries}{self.parts.fragment}'

        return f'{self.parts.scheme}://{self.parts.netloc}{self.parts.path}{self.parts.fragment}'

    def init_base_url_alternative(self):
        """
        Set alternative base url including or excluding slash at the end of it depending on original URL
        """
        
        if '/' == self.parts.path:
            self.alternative_base_url = URL(f'{self.parts.scheme}://{self.parts.netloc}')
        else:
            self.alternative_base_url = URL(f'{self.parts.scheme}://{self.parts.netloc}{self.parts.params}')

    def __format_url(self, url: str, base_url: str):
        """
        Format the URL properly
        :param url: new URL
        :base_url: original URL
        :return: 
            - original URL if the new one contains only \"#\"
            - original URL concatenate with current URL if the new one starts with \"/\"
            - new URL if it starts with \"http\"
            - concatenation of original URL + \"/\" + new URL, otherwise
        """

        if '#' == url:
            return base_url
        
        if url.startswith('/'):
            if base_url.endswith('/'):
                return f'{base_url[:-1]}{url}'
            return f'{base_url}{url}'
        
        if url.startswith('http'):
            return f'{url}'
        
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
        if self.is_same_domain(second_url):
            # test if paths are the same 
            if second_url.parts.path == self.parts.path:
                return True
        
            # test if the only difference is the final slash
            if ('/' == second_url.parts.path and '' == self.parts.path) or ('/' == self.parts.path and '' == second_url.parts.path):
                return True
        
        return False

    def is_same_domain(self, second_url: URL):
        """
        Check if two URLs have the same domain
        :param second_url: second URL
        :return: True if two resources have the same domain, False otherwise
        """

        second_url_domain = domain_extractor(second_url.parts.netloc)
        url_domain = domain_extractor(self.parts.netloc)

        # skip comparing www subdomain
        if (('www' not in [ second_url_domain.subdomain, url_domain.domain ]) and ('' not in [ second_url_domain.subdomain, url_domain.domain ]) and (second_url_domain.subdomain != url_domain.domain)): 
            return False

        return second_url_domain.domain == url_domain.domain and second_url_domain.suffix == url_domain.suffix
