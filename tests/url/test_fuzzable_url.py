import unittest

from urlfinder.core.url import URL

class TestFuzzable(unittest.TestCase):
    def test_no_parameter(self):
        url = URL('https://asdf.com')
        self.assertFalse(url.is_fuzzable())

    def test_no_parameter_with_slash(self):
        url = URL('https://asdf.com/')
        self.assertFalse(url.is_fuzzable())

    def test_no_parameter_with_resource(self):
        url = URL('https://asdf.com/test.php')
        self.assertFalse(url.is_fuzzable())

    def test_single_fuzzable_parameter(self):
        url = URL('https://asdf.com/?test=hello')
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_empty_parameter(self):
        url = URL('https://asdf.com/?test=')
        self.assertTrue(url.is_fuzzable())

    def test_single_paramenter_without_equal(self):
        url = URL('https://asdf.com/?test')
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters(self):
        url = URL('https://asdf.com/?test=hello&test2=world')
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters_single_empty(self):
        url = URL('https://asdf.com/?test=&test2=world')
        self.assertTrue(url.is_fuzzable())

    def test_single_fuzzable_parameters_empty_values(self):
        url = URL('https://asdf.com/?test=&test2=')
        self.assertTrue(url.is_fuzzable())

if __name__ == '__main__':
    unittest.main()
