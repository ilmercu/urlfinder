import unittest

from urlfinder.core.elements.url import URL
from urlfinder.core.url_parser import URLParser

class TestHumanPrintable(unittest.TestCase):
    def test_success_print_main_url(self):
        main_url = 'https://acde.com'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_with_slash(self):
        main_url = 'https://acde.com/'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_main_url_with_resource(self):
        main_url = 'https://acde.com/test.php'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_single_parameter(self):
        main_url = 'https://acde.com/test.php?test=hello'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_with_parameters(self):
        main_url = 'https://acde.com/test.php?test=hello&test2=world'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_single_parameter_empty(self):
        main_url = 'https://acde.com/test.php?test='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_parameter_without_equal(self):
        main_url = 'https://acde.com/test.php?test'
        desired_url = f'{main_url}='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), desired_url)

    def test_success_print_multi_parameters_empty_value(self):
        main_url = 'https://acde.com/test.php?test=&test2=notempty'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

    def test_success_print_empty_parameters(self):
        main_url = 'https://acde.com/test.php?test=&test2='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_value(), main_url)

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

    def test_success_encoded_parameter_space_plus(self):
        base_url = 'https://jklqwe.com/test_test2/test.html?q1=test+test2'
        url_parser = URLParser(base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), base_url)

    def test_success_encoded_parameter_space_utf8(self):
        base_url = 'https://jklqwe.com/test_test2/test.html?q1=test%20test2'
        url_parser = URLParser(base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), base_url)

    def test_success_encoded_path_space_plus(self):
        base_url = 'https://jklqwe.com/test+test2/test.html'
        url_parser = URLParser(base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), base_url)

    def test_success_encoded_path_space_utf8(self):
        base_url = 'https://jklqwe.com/test%20test2/test.html'
        url_parser = URLParser(base_url)
        url_obj_1 = URL(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), base_url)

if __name__ == '__main__':
    unittest.main()
 