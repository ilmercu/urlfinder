from urllib.parse import ParseResult


class Phone:
    """
    This class represents a phone instance coming from an URL (including a possible "tel protocol")
    """

    def __init__(self, parts: ParseResult):
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.get_phone())
    
    def __str__(self):
        return self.get_phone()

    def get_phone(self) -> str:
        """
        Get human readble phone number
        
        :return: human readable phone number
        """

        return self.parts.path
