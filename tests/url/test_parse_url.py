import unittest

from urlfinder.core.elements.url import URL
from urlfinder.core.url_parser import URLParser

class TestParseURL(unittest.TestCase):
    def test_success_complete_url(self):
        url_1 = 'https://asdf.com'
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_slash(self):
        url_1 = 'https://asdf.com/'
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_path(self):
        url_1 = 'https://asdf.com/test'
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_param(self):
        url_1 = 'https://asdf.com/test.php?test=hello'
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_empty_param(self):
        url_1 = 'https://asdf.com/test.php?test='
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_empty_param_and_params(self):
        url_1 = 'https://asdf.com/test.php?test=&test2=hello'
        url_parser = URLParser(url_1)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_complete_url_with_base_url_and_complete_url(self):
        base_url = 'https://jklqwe.com'
        url_1 = 'https://asdf.com'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_with_base_url_and_absolute_url(self):
        base_url = 'https://jklqwe.com'
        url_1 = '/asdf'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1}')

    def test_success_with_base_url_and_double_slash_url(self):
        base_url = 'https://jklqwe.com'
        url_1 = '//ertyui.com'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'https:{url_1}')

    def test_success_with_base_url_and_empty_fragment(self):
        base_url = 'https://jklqwe.com'
        url_1 = '#'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), base_url)

    def test_success_with_base_url_and_fragment(self):
        base_url = 'https://jklqwe.com'
        url_1 = '#hello'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1}')

    def test_success_with_base_url_and_query(self):
        base_url = 'https://jklqwe.com'
        url_1 = '?test=hello'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1}')

    def test_success_with_base_url_and_query_and_fragment(self):
        base_url = 'https://jklqwe.com'
        url_1 = '?test=hello#hello'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1}')

    def test_exception_invalid_url_no_base_url(self):
        url_1 = 'test'
        with self.assertRaises(AttributeError): 
            URLParser(url_1)

    def test_exception_absolute_url_no_base_url(self):
        url_1 = '/test'
        with self.assertRaises(AttributeError): 
            URLParser(url_1)

    def test_exception_malformed_url(self):
        url_1 = 'https:/test'
        with self.assertRaises(AttributeError): 
            URLParser(url_1)

    def test_success_with_single_dot_relative_path(self):
        base_url = 'https://jklqwe.com'
        url_1 = './test'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1[1:]}')

    def test_success_with_double_dot_relative_path(self):
        base_url = 'https://jklqwe.com'
        url_1 = '../test'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}/{url_1}')

    def test_success_with_slash_and_double_dot_relative_path(self):
        base_url = 'https://jklqwe.com/'
        url_1 = '../test'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), f'{base_url}{url_1}')
        
if __name__ == '__main__':
    unittest.main()
 
