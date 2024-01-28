import unittest

from urlfinder.core.url import URL
from urlfinder.core.url_parser import URLParser

class TestFuzzPrintable(unittest.TestCase):
    def test_success_print_main_url(self):
        main_url = 'https://acde.com'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_with_slash(self):
        main_url = 'https://acde.com/'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_main_url_with_resource(self):
        main_url = 'https://acde.com/test.php'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_single_parameter(self):
        main_url = 'https://acde.com/test.php?test=hello'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_with_parameters(self):
        main_url = 'https://acde.com/test.php?test=hello&test2=world'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_single_parameter_empty(self):
        main_url = 'https://acde.com/test.php?test='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_parameter_without_equal(self):
        main_url = 'https://acde.com/test.php?test'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_multi_parameters_empty_value(self):
        main_url = 'https://acde.com/test.php?test=&test2=notempty'
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_empty_parameters(self):
        main_url = 'https://acde.com/test.php?test=&test2='
        url_parser = URLParser(main_url)
        url = URL(url_parser.get_parts())
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

if __name__ == '__main__':
    unittest.main()
 