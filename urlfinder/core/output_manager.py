from os import makedirs, path

from enum import Enum

class OutputManagerEnum(Enum):
    BASE_PATH = './output'
    URLS_LIST_OUTPUT_FILENAME = 'urls-complete-list.txt'
    FUZZABLE_URLS_OUTPUT_FILENAME = 'fuzzable-urls.txt'
    MAIL_OUTPUT_FILENAME = 'mails.txt'


class OutputManager:
    def __init__(self, domain: str):
        """
        Return new OutputManager instance creating also destination filepaths
        """

        self.base_path = f'{OutputManagerEnum.BASE_PATH.value}/{domain}/'
        self.__create_destination_path()

    def __create_destination_path(self):
        """
        Create destination filepaths
        """

        filepaths = [ 
            f'{self.base_path}/{OutputManagerEnum.URLS_LIST_OUTPUT_FILENAME.value}', 
            f'{self.base_path}/{OutputManagerEnum.FUZZABLE_URLS_OUTPUT_FILENAME.value}', 
            f'{self.base_path}/{OutputManagerEnum.MAIL_OUTPUT_FILENAME.value}'
        ]

        try:
            for filepath in filepaths:
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

    def write(self, filepath: OutputManagerEnum, line: str):
        """
        Write content inside a file
        :parameter filepath: destination file
        :parameter line: content to write
        """

        try:
            with open(f'{self.base_path}/{filepath.value}', 'a') as f:
                f.write(f'{line}\n')
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied')
            exit(1)
