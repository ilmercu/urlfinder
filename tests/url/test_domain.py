import unittest

from urlfinder.core.url import URL

class TestDomain(unittest.TestCase):
    def test_success_same_url(self):
        url_1 = URL('https://asdf.com')
        url_2 = URL('https://asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))

    def test_success_without_single_www(self):
        url_1 = URL('https://asdf.com')
        url_2 = URL('https://www.asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))

    def test_success_without_inverted_single_www(self):
        url_1 = URL('https://www.asdf.com')
        url_2 = URL('https://asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))

    def test_success_different_subdomain(self):
        url_1 = URL('https://abc.asdf.com')
        url_2 = URL('https://asdf.com')
        self.assertFalse(url_1.is_same_domain(url_2))
    
    def test_success_different_protocol(self):
        url_1 = URL('http://www.asdf.com/xyz')
        url_2 = URL('https://www.asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))
    
    def test_success_different_resource(self):
        url_1 = URL('https://www.asdf.com/shop/')
        url_2 = URL('https://www.asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))
    
    def test_success_different_resource_and_subdomain(self):
        url_1 = URL('https://www.asdf.com/shop/')
        url_2 = URL('https://asdf.com')
        self.assertTrue(url_1.is_same_domain(url_2))
    
    def test_success_different_resources_and_subdomain(self):
        url_1 = URL('https://www.asdf.com/shop/')
        url_2 = URL('https://asdf.com/test')
        self.assertTrue(url_1.is_same_domain(url_2))

if __name__ == '__main__':
    unittest.main()
