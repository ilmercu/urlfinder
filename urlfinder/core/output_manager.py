from os import makedirs, path

from enum import Enum

class OutputManagerEnum(Enum):
    URLS_LIST_OUTPUT_FILEPATH = './output/urls-complete-list.txt'
    FUZZABLE_URLS_OUTPUT_FILEPATH = './output/fuzzable-urls.txt'
    MAIL_OUTPUT_FILEPATH = './output/mails.txt'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class OutputManager:
    def __init__(self):
        """
        Return new OutputManager instance creating also destination filepaths
        """

        self.__create_destination_path()

    def __create_destination_path(self):
        """
        Create destination filepaths
        """

        try:
            for filepath in OutputManagerEnum.list():
                makedirs(path.dirname(filepath), exist_ok=True)
                
                # create empty file
                with open(filepath, 'w') as f:
                    pass
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied or file/folder already exists with the same name')
            exit(1)
        except FileExistsError as e:
            print(f'Error creating destination filepath. File or folder with the same name already exists')
            exit(1)

    def write(self, filepath: str, line: str):
        """
        Write content inside a file
        :parameter filepath: destination file
        :parameter line: content to write
        """

        try:
            with open(filepath, 'a') as f:
                f.write(f'{line}\n')
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied')
            exit(1)
