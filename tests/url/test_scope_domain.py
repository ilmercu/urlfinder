import unittest

from urlfinder.core.elements.url import URL
from urlfinder.core.url_parser import URLParser

class TestScopeDomain(unittest.TestCase):
    def test_success_same_url(self):
        url = 'https://asdf.com'
        url_parser = URLParser(url)
        url_obj = URL(url_parser.get_parts())
        scope_domains = set()
        url_2 = 'asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj.is_in_scope(scope_domains))

    def test_success_with_single_www(self):
        url_1 = 'https://www.asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())

        scope_domains = set()
        url_2 = 'asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj_1.is_in_scope(scope_domains))

    def test_success_with_double_www(self):
        url_1 = 'https://www.asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())

        scope_domains = set()
        url_2 = 'www.asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj_1.is_in_scope(scope_domains))

    def test_success_with_double_subdomain(self):
        url_1 = 'https://test.asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())

        scope_domains = set()
        url_2 = 'test.asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj_1.is_in_scope(scope_domains))

    def test_success_multi_domain(self):
        url_1 = 'https://asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())

        scope_domains = set()
        url_2 = 'zxcvlkjh.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        url_3 = 'www.asdf.com'
        url_parser_3 = URLParser(url_3, is_scope_domain=True)
        url_obj_3 = URL(url_parser_3.get_parts())
        scope_domains.add(url_obj_3)
        self.assertTrue(url_obj_1.is_in_scope(scope_domains))

    def test_fail_not_in_scope(self):
        url = 'https://asdf.com'
        url_parser = URLParser(url)
        url_obj = URL(url_parser.get_parts())

        scope_domains = set()
        url_2 = 'zxcvlkjh.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        url_3 = 'www.lmkexerqpqw.com'
        url_parser_3 = URLParser(url_3, is_scope_domain=True)
        url_obj_3 = URL(url_parser_3.get_parts())
        scope_domains.add(url_obj_3)
        self.assertFalse(url_obj.is_in_scope(scope_domains))

    def test_success_no_subdomain_with_wildcard(self):
        url = 'https://asdf.com'
        url_parser = URLParser(url)
        url_obj = URL(url_parser.get_parts())

        scope_domains = set()
        url_2 = '*.asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj.is_in_scope(scope_domains))

    def test_success_with_subdomain_with_wildcard(self):
        url = 'https://xyz.asdf.com'
        url_parser = URLParser(url)
        url_obj = URL(url_parser.get_parts())

        scope_domains = set()
        url_2 = '*.asdf.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertTrue(url_obj.is_in_scope(scope_domains))

    def test_fail_with_subdomain_not_in_scope(self):
        url = 'https://xyz.asdf.com'
        url_parser = URLParser(url)
        url_obj = URL(url_parser.get_parts())

        scope_domains = set()
        url_2 = '*.zxcvlkjh.com'
        url_parser_2 = URLParser(url_2, is_scope_domain=True)
        url_obj_2 = URL(url_parser_2.get_parts())
        scope_domains.add(url_obj_2)
        self.assertFalse(url_obj.is_in_scope(scope_domains))

if __name__ == '__main__':
    unittest.main()
