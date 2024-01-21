from os import makedirs, path

from enum import Enum

class OutputManagerEnum(Enum):
    URLS_LIST_OUTPUT_FILEPATH = './output/urls-complete-list.txt'
    FUZZABLE_URLS_OUTPUT_FILEPATH = './output/fuzzable-urls.txt'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class OutputManager:
    def __init__(self):
        self.__create_destination_path()

    def __create_destination_path(self):
        for filepath in OutputManagerEnum.list():
            makedirs(path.dirname(filepath), exist_ok=True)
            
            # create empty file
            try:
                with open(filepath, 'w') as f:
                    pass
            except PermissionError as e:
                print(f'Error writing {e.filename}. Permission denied or file/folder already exists with the same name')

    def write(self, filepath: str, line: str):
        try:
            with open(filepath, 'a') as f:
                f.write(f'{line}\n')
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied')
