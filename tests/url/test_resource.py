import unittest

from urlfinder.core.url import URL

class TestResource(unittest.TestCase):
    def test_success_same_resource_no_slash(self):
        url_1 = URL('https://xcvber.com')
        url_2 = URL('https://xcvber.com')
        self.assertTrue(url_1.is_same_resource(url_2))

    def test_success_same_resource_one_slash(self):
        url_1 = URL('https://xcvber.com/')
        url_2 = URL('https://xcvber.com')
        self.assertTrue(url_1.is_same_resource(url_2))

    def test_success_same_resource_other_slash(self):
        url_1 = URL('https://xcvber.com')
        url_2 = URL('https://xcvber.com/')
        self.assertTrue(url_1.is_same_resource(url_2))

    def test_same_resource_with_single_www(self):
        url_1 = URL('https://xcvber.com')
        url_2 = URL('https://www.xcvber.com')
        self.assertTrue(url_1.is_same_resource(url_2))

    def test_same_resource_with_double_www(self):
        url_1 = URL('https://www.xcvber.com')
        url_2 = URL('https://www.xcvber.com')
        self.assertTrue(url_1.is_same_resource(url_2))

    def test_different_resource_domain(self):
        url_1 = URL('https://xcvber.com')
        url_2 = URL('https://instagram.com')
        self.assertFalse(url_1.is_same_resource(url_2))

    def test_different_resource_without_single_path(self):
        url_1 = URL('https://xcvber.com')
        url_2 = URL('https://xcvber.com/abcdef')
        self.assertFalse(url_1.is_same_resource(url_2))

    def test_different_resource_with_paths(self):
        url_1 = URL('https://www.xcvber.it/dove-siamo/')
        url_2 = URL('https://www.xcvber.it/carrello/')
        self.assertFalse(url_1.is_same_resource(url_2))

    def test_different_resource_subdomain_with_paths(self):
        url_1 = URL('https://test.xcvber.it/dove-siamo/')
        url_2 = URL('https://www.xcvber.it/carrello/')
        self.assertFalse(url_1.is_same_resource(url_2))

if __name__ == '__main__':
    unittest.main()
