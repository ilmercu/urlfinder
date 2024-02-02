from urllib.parse import ParseResult


class BaseElement:
    """
    This class represents the base instance of an URL (real URL, mail, phone), including its protocol
    """

    def __init__(self, parts: ParseResult):
        """
        Return new element instance

        :param parts: parts of the new URL
        """

        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.get_value())
    
    def __str__(self):
        return self.get_value()

    def get_value(self) -> str:
        """
        Get human readble value containing the path of the URL
        
        :return: human readable path
        """

        return self.parts.path
