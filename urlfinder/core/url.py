from __future__ import annotations
from urllib.parse import ParseResult, quote_plus
from tldextract import extract as domain_extractor

class URL:
    """
    This class represent an URL
    """
    
    def __init__(self, parts: ParseResult):
        """
        Return new URL instance

        :param parts: parts of the new URL
        """
        
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.get_url(fuzz_parameters=True))
    
    def __str__(self):
        return self.get_url()
    
    @classmethod
    def extract_domain(cls, url: URL):
        return domain_extractor(url.parts.netloc)

    def get_url(self, fuzz_parameters: bool=False) -> str:
        """
        Get human readble or fuzzed format URL

        :param fuzz_parameters: True if the return value will contain replaced query values, False otherwise
        :return: human readable URL or fuzzed parameters URL 
        """
        
        queries = ''
        if self.parts.query:
            # compose query
            i = 0
            for query in self.parts.query:
                
                if fuzz_parameters:
                    queries += f'{query[0]}=FUZZ{i}&'
                else:
                    query_parameter = f'{query[0]}='
                    if query[1]:
                       query_parameter = f'{query_parameter}{quote_plus(query[1])}'
                    queries += f'{query_parameter}&'
                i += 1

            # removing last &
            queries = f'?{queries[:-1]}'
        
        fragment = ''
        if self.parts.fragment:
            fragment = f'#{self.parts.fragment}'
        
        return f'{self.parts.scheme}://{self.parts.netloc}{self.parts.path}{queries}{fragment}'
    
    def is_same_resource(self, second_url: URL) -> bool:
        """
        Check if two URLs are the same

        :param second_url: second URL
        :return: True if two resources are the same, False otherwise
        """

        # test if objects are the same
        if second_url == self:
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

    def is_same_domain(self, second_url: URL) -> bool:
        """
        Check if two URLs have the same domain

        :param second_url: second URL
        :return: True if two resources have the same domain, False otherwise
        """

        second_url_domain = URL.extract_domain(second_url)
        url_domain = URL.extract_domain(self)

        if second_url_domain.subdomain == url_domain.subdomain and second_url_domain.domain == url_domain.domain and second_url_domain.suffix == url_domain.suffix:
            return True
        
        if 'www' in [ second_url_domain.subdomain, url_domain.subdomain ] and '' in [ second_url_domain.subdomain, url_domain.subdomain ] and second_url_domain.domain == url_domain.domain:
            return True

        return False
    
    def is_fuzzable(self):
        """
        Return if an URL can be fuzzable

        :return: True if the URL contains a set of parameters, False otherwise
        """
        
        if self.parts.query:
            return True
        
        return False

    def is_in_scope(self, scope_domains: set):
        """
        Return if an URL is in scope
        
        :param scope_domains: domains in scope
        :return: True if the URL is in scope, False otherwise
        """
        
        url_domain = URL.extract_domain(self)

        for domain in scope_domains:
            if self.is_same_domain(domain):
                return True
            
            # check for wildcard
            scope_domain = URL.extract_domain(domain)

            if '*' == scope_domain.subdomain and \
                url_domain.domain == scope_domain.domain and \
                url_domain.suffix == scope_domain.suffix:
                return True

        return False
        
