import os
import json
from core.saltlux.utils import get_path
from typing import Dict


class CommonResource:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
        self.config = self._load_config()
        self.directories = self.config['directories']
        self.preprocess = self.config['preprocess']

    @property
    def data_dir(self) -> str:
        return get_path(self.root_dir, self.directories['database_dir'], self.directories['data_dir'])

    @property
    def preprocess_dir(self) -> str:
        return get_path(self.root_dir, self.directories['database_dir'], self.directories['preprocess_dir'])

    @property
    def preprocess_config(self) -> Dict:
        return self.preprocess

    def _load_config(self) -> Dict:
        with open(get_path(self.root_dir, 'config.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config

if __name__ == '__main__':
    resource = CommonResource()

    print(resource.root_dir)
    print(resource.config)
    print(resource.data_dir)
    print(resource.preprocess_dir)