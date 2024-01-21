import unittest

from urlfinder.core.url import URL

class TestPrintable(unittest.TestCase):
    def test_success_print_main_url(self):
        main_url = 'https://acde.com'
        url = URL(main_url)
        self.assertEqual(url.get_url(), main_url)

    def test_success_print_main_url_with_resource(self):
        main_url = 'https://acde.com/test.php'
        url = URL(main_url)
        self.assertEqual(url.get_url(), main_url)

    def test_success_print_with_slash(self):
        main_url = 'https://acde.com/'
        url = URL(main_url)
        self.assertEqual(url.get_url(), main_url)

    def test_success_print_single_parameter(self):
        main_url = 'https://acde.com/test.php?test=hello'
        url = URL(main_url)
        self.assertEqual(url.get_url(), main_url)

    def test_success_print_with_parameters(self):
        main_url = 'https://acde.com/test.php?test=hello&test2=world'
        url = URL(main_url)
        # swap parameters since set doesn't keep insertion order
        url_swapped_params = 'https://acde.com/test.php?test2=world&test=hello'
        result = url.get_url() in [ main_url, url_swapped_params ]
        self.assertTrue(result)

    def test_success_print_single_parameter_empty(self):
        main_url = 'https://acde.com/test.php?test='
        url = URL(main_url)
        # swap parameters since set doesn't keep insertion order
        url_swapped_params = 'https://acde.com/test.php?test='
        result = url.get_url() in [ main_url, url_swapped_params ]
        self.assertTrue(result)

    def test_success_print_multi_parameters_empty_value(self):
        main_url = 'https://acde.com/test.php?test=&test2=notempty'
        url = URL(main_url)
        # swap parameters since set doesn't keep insertion order
        url_swapped_params = 'https://acde.com/test.php?test2=notempty&test='
        result = url.get_url() in [ main_url, url_swapped_params ]
        self.assertTrue(result)

    def test_success_print_multi_parameters_empty_value(self):
        main_url = 'https://acde.com/test.php?test'
        url = URL(main_url)
        desired_url = f'{main_url}='
        self.assertEqual(url.get_url(), desired_url)

    def test_success_print_empty_parameters(self):
        main_url = 'https://acde.com/test.php?test=&test2='
        url = URL(main_url)
        url_swapped_params = 'https://acde.com/test.php?test2=&test='
        result = url.get_url() in [ main_url, url_swapped_params ]
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
 