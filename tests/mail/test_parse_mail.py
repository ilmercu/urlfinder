import unittest

from urlfinder.core.elements.base_element import BaseElement
from urlfinder.core.url_parser import URLParser

class TestParseMail(unittest.TestCase):
    def test_success_is_mail(self):
        main_url = 'mailto:abc@abc.com'
        url_parser = URLParser(main_url)
        self.assertTrue(url_parser.is_mail())

    def test_success_is_mail_with_parameters(self):
        main_url = 'mailto:abc@abc.com?cc=someone'
        url_parser = URLParser(main_url)
        self.assertTrue(url_parser.is_mail())

    def test_fail_no_protocol(self):
        main_url = 'abc@abc.com'
        url_parser = URLParser(main_url)
        self.assertTrue(url_parser.is_mail())

    def test_fail_missing_mail(self):
        main_url = 'mailto:?body=body&subject=subject'
        with self.assertRaises(AttributeError): 
            URLParser(main_url)
        
if __name__ == '__main__':
    unittest.main()
 