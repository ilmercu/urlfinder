import unittest

from urlfinder.core.elements.url import URL
from urlfinder.core.url_parser import URLParser

class TestResource(unittest.TestCase):
    def test_success_same_resource_no_slash(self):
        url_1 = 'https://xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://xcvber.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_resource(url_obj_2))

    def test_success_same_resource_one_slash(self):
        url_1 = 'https://xcvber.com/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://xcvber.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_resource(url_obj_2))

    def test_success_same_resource_other_slash(self):
        url_1 = 'https://xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://xcvber.com/'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_resource(url_obj_2))

    def test_success_same_resource_with_single_www(self):
        url_1 = 'https://xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.xcvber.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_resource(url_obj_2))

    def test_success_same_resource_with_double_www(self):
        url_1 = 'https://www.xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.xcvber.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertTrue(url_obj_1.is_same_resource(url_obj_2))

    def test_fail_different_resource_domain(self):
        url_1 = 'https://xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://lkjh.com'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertFalse(url_obj_1.is_same_resource(url_obj_2))

    def test_fail_different_resource_without_single_path(self):
        url_1 = 'https://xcvber.com'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://xcvber.com/abcdef'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertFalse(url_obj_1.is_same_resource(url_obj_2))

    def test_fail_different_resource_with_paths(self):
        url_1 = 'https://www.xcvber.it/dove-siamo/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.xcvber.it/carrello/'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertFalse(url_obj_1.is_same_resource(url_obj_2))

    def test_fail_different_resource_subdomain_with_paths(self):
        url_1 = 'https://test.xcvber.it/dove-siamo/'
        url_parser_1 = URLParser(url_1)
        url_obj_1 = URL(url_parser_1.get_parts())
        url_2 = 'https://www.xcvber.it/carrello/'
        url_parser_2 = URLParser(url_2)
        url_obj_2 = URL(url_parser_2.get_parts())
        self.assertFalse(url_obj_1.is_same_resource(url_obj_2))

if __name__ == '__main__':
    unittest.main()
