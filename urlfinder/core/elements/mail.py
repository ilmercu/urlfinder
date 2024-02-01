from urllib.parse import ParseResult


class Mail:
    """
    This class represents a mail instance coming from an URL (including a possible "mailto protocol")
    """

    def __init__(self, parts: ParseResult):
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.get_mail())
    
    def __str__(self):
        return self.get_mail()

    def get_mail(self) -> str:
        """
        Get human readble mail
        
        :return: human readable mail
        """

        return self.parts.path
