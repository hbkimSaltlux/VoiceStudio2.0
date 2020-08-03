import threading
from core.saltlux.utils import get_dir_list
from typing import Dict, NoReturn

lock = threading.Lock()

class PreprocessResource:
    def __init__(self, working_dir: str, configs: Dict):
        self.working_dir = working_dir
        self.resources = self._load_resources()
        self.configs = configs

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
            self.resources = self._load_resources()

    def is_valid_key(self, key: str) -> bool:
        return key in self.resources.keys()


if __name__ == '__main__':
    resource = PreprocessResource('/data1/speech-team/hbkim/voice_studio_2.0/core/saltlux/database/preprocess')

    print(resource.resources)
    print(resource.is_valid_key('preDataset200803104352435890'))
    print(resource.working_dir)