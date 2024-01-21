import unittest

from urlfinder.core.url import URL

class TestFuzzPrintable(unittest.TestCase):
    def test_success_print_main_url(self):
        main_url = 'https://acde.com'
        url = URL(main_url)
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_with_slash(self):
        main_url = 'https://acde.com/'
        url = URL(main_url)
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_main_url_with_resource(self):
        main_url = 'https://acde.com/test.php'
        url = URL(main_url)
        self.assertEqual(url.get_url(fuzz_parameters=True), main_url)

    def test_success_print_single_parameter(self):
        main_url = 'https://acde.com/test.php?test=hello'
        url = URL(main_url)
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_with_parameters(self):
        main_url = 'https://acde.com/test.php?test=hello&test2=world'
        url = URL(main_url)
        # swap parameters since set doesn't keep insertion order
        desired_fuzz_1 = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        desired_fuzz_2 = 'https://acde.com/test.php?test2=FUZZ0&test=FUZZ1'
        desired_fuzz_3 = 'https://acde.com/test.php?test=FUZZ1&test2=FUZZ0'
        desired_fuzz_4 = 'https://acde.com/test.php?test2=FUZZ1&test=FUZZ0'
        result = url.get_url(fuzz_parameters=True) in [ desired_fuzz_1, desired_fuzz_2, desired_fuzz_3, desired_fuzz_4 ]
        self.assertTrue(result)

    def test_success_print_single_parameter_empty(self):
        main_url = 'https://acde.com/test.php?test='
        url = URL(main_url)
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_parameter_without_equal(self):
        main_url = 'https://acde.com/test.php?test'
        url = URL(main_url)
        desired_fuzz = 'https://acde.com/test.php?test=FUZZ0'
        self.assertEqual(url.get_url(fuzz_parameters=True), desired_fuzz)

    def test_success_print_multi_parameters_empty_value(self):
        main_url = 'https://acde.com/test.php?test=&test2=notempty'
        url = URL(main_url)
        desired_fuzz_1 = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        desired_fuzz_2 = 'https://acde.com/test.php?test2=FUZZ0&test=FUZZ1'
        desired_fuzz_3 = 'https://acde.com/test.php?test=FUZZ1&test2=FUZZ0'
        desired_fuzz_4 = 'https://acde.com/test.php?test2=FUZZ1&test=FUZZ0'
        result = url.get_url(fuzz_parameters=True) in [ desired_fuzz_1, desired_fuzz_2, desired_fuzz_3, desired_fuzz_4 ]
        self.assertTrue(result)

    def test_success_print_empty_parameters(self):
        main_url = 'https://acde.com/test.php?test=&test2='
        url = URL(main_url)
        desired_fuzz_1 = 'https://acde.com/test.php?test=FUZZ0&test2=FUZZ1'
        desired_fuzz_2 = 'https://acde.com/test.php?test2=FUZZ0&test=FUZZ1'
        desired_fuzz_3 = 'https://acde.com/test.php?test=FUZZ1&test2=FUZZ0'
        desired_fuzz_4 = 'https://acde.com/test.php?test2=FUZZ1&test=FUZZ0'
        result = url.get_url(fuzz_parameters=True) in [ desired_fuzz_1, desired_fuzz_2, desired_fuzz_3, desired_fuzz_4 ]
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
 