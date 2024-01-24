import unittest

from urlfinder.core.url import URL
from urlfinder.core.url_parser import URLParser

class TestDomain(unittest.TestCase):
    def test_success_same_url(self):
        url_1 = 'https://asdf.com'
        url_2 = url_1
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))

    def test_success_without_single_www(self):
        url_1 = 'https://asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))

    def test_success_without_inverted_single_www(self):
        url_1 = 'https://www.asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))

    def test_success_different_subdomain(self):
        url_1 = 'https://abc.asdf.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertFalse(url_obj_1.is_same_domain(url_obj_2))
    
    def test_success_different_protocol(self):
        url_1 = 'http://www.asdf.com/xyz'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))
    
    def test_success_different_resource(self):
        url_1 = 'https://www.asdf.com/shop/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))
    
    def test_success_different_resource_and_subdomain(self):
        url_1 = 'https://www.asdf.com/shop/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://asdf.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))
    
    def test_success_different_resources_and_subdomain(self):
        url_1 = 'https://www.asdf.com/shop/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://asdf.com/test'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_domain(url_obj_2))

if __name__ == '__main__':
    unittest.main()
