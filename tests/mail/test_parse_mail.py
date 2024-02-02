import unittest

from urlfinder.core.elements.base_element import BaseElement
from urlfinder.core.url_parser import URLParser

class TestMail(unittest.TestCase):
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

    def test_missing_mail(self):
        main_url = 'mailto:?body=body&subject=subject'
        with self.assertRaises(AttributeError): 
            URLParser(main_url)

    def test_get_mail_with_protocol(self):
        current_mail = 'abc@abc.com'
        main_url = f'mailto:{current_mail}'
        url_parser = URLParser(main_url)
        mail = BaseElement(url_parser.get_parts())
        self.assertEqual(mail.get_value(), current_mail)

    def test_get_mail_without_protocol(self):
        main_url = 'abc@abc.com'
        url_parser = URLParser(main_url)
        mail = BaseElement(url_parser.get_parts())
        self.assertEqual(mail.get_value(), main_url)

    def test_get_mail_with_parameters(self):
        current_mail = 'abc@abc.com'
        main_url = f'mailto:{current_mail}?cc=someone'
        url_parser = URLParser(main_url)
        mail = BaseElement(url_parser.get_parts())
        self.assertEqual(mail.get_value(), current_mail)

    def test_success_parse_mail_with_base_url(self):
        base_url = 'https://jklqwe.com'
        url_1 = 'test@test.com'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = BaseElement(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), url_1)

    def test_success_parse_mail_with_protocol_and_base_url(self):
        base_url = 'https://jklqwe.com'
        mail = 'test@test.com'
        url_1 = f'mailto:{mail}'
        url_parser = URLParser(url_1, base_url)
        url_obj_1 = BaseElement(url_parser.get_parts())
        self.assertEqual(url_obj_1.get_value(), mail)
        
if __name__ == '__main__':
    unittest.main()
 