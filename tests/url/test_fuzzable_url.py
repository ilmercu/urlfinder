import unittest

from urlfinder.core.url import URL
from core.url_parser import URLParser

class TestFuzzable(unittest.TestCase):
    def test_no_parameter(self):
        main_url = 'https://asdf.com'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertFalse(url.is_fuzzable())

    def test_no_parameter_with_slash(self):
        main_url = 'https://asdf.com/'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertFalse(url.is_fuzzable())

    def test_no_parameter_with_resource(self):
        main_url = 'https://asdf.com/test.php'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertFalse(url.is_fuzzable())

    def test_single_fuzzable_parameter(self):
        main_url = 'https://asdf.com/?test=hello'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_empty_parameter(self):
        main_url = 'https://asdf.com/?test='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

    def test_single_paramenter_without_equal(self):
        main_url = 'https://asdf.com/?test'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters(self):
        main_url = 'https://asdf.com/?test=hello&test2=world'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters_single_empty(self):
        main_url = 'https://asdf.com/?test=&test2=world'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters_empty_values(self):
        main_url = 'https://asdf.com/?test=&test2='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertTrue(url.is_fuzzable())

if __name__ == '__main__':
    unittest.main()
