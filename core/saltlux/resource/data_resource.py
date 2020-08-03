import threading
from core.saltlux.utils import get_dir_list
from typing import Dict, NoReturn

lock = threading.Lock()

class DataResource:
    def __init__(self, working_dir: str):
        self.working_dir = working_dir
        self.resources = self._load_resources()

    def _load_resources(self) -> Dict:
        dir_list = get_dir_list(self.working_dir)

        resources = {}
        for dir in dir_list:
            tokens = dir.split('_')
            key = tokens[0]
            name = ' '.join(tokens[1:])
            resources[key] = {'name': name}

        return resources

    def refresh(self) -> NoReturn:
        with lock:
            self._load_resources()

    def is_valid_key(self, key: str) -> bool:
        return key in self.resources.keys()

    def get_dataset_name(self, key: str) -> str:
        return self.resources[key]['name']




if __name__ == '__main__':
    resource = DataResource('/data1/speech-team/hbkim/voice_studio_2.0/core/saltlux/database/data')

    print(resource.is_valid_key('dataset200723110932806189'))
