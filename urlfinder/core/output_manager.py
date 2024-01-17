from os import makedirs, path
from ..config.config import DEFAULT_OUTPUT_FILENAME

class OutputManager:
    def __init__(self, destination_path: str):
        self.destination_path = destination_path
        self.__create_destination_path()

    def __create_destination_path(self):    
        if path.dirname(self.destination_path) and path.dirname(self.destination_path) not in [ '.', '/', './' ]:
            makedirs(path.dirname(self.destination_path), exist_ok=True)
            
            if path.basename(self.destination_path):
                self.destination_path = f'{path.dirname(self.destination_path)}/{path.basename(self.destination_path)}'
            else:
                self.destination_path = f'{self.destination_path}/{DEFAULT_OUTPUT_FILENAME}'
        
        # create empty file
        try:
            with open(self.destination_path, 'w') as f:
                pass
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied or file/folder already exists')

    def write(self, line: str):
        try:
            with open(self.destination_path, 'a') as f:
                f.write(f'{line}\n')
        except PermissionError as e:
            print(f'Error writing {e.filename}. Permission denied or file/folder already exists')