import threading
import os
import shutil
from typing import NoReturn
from datetime import datetime

key_lock = threading.Lock()


def generate_key(key_prefix: str) -> str:
    with key_lock:
        key_suffix = datetime.now().strftime('%Y%m%d%H%M%S%f')

    key = key_prefix + key_suffix[2:]
    return key


def get_dir_list(path: str) -> str:
    return os.listdir(path)


def get_dir_name(key: str, name: str) -> str:
    name = name.replace(' ', '_')
    dir_name = '{}_{}'.format(key, name)
    return dir_name


def get_path(*paths: str, makedir: bool = False) -> str:
    path = os.path.join(*paths)
    if makedir:
        make_dirs(path)

    return os.path.join(*paths)


def make_dirs(path: str) -> bool:
    if not is_exists(path):
        os.makedirs(path, exist_ok=True)
        return True

    return False


def remove_dirs(path: str) -> bool:
    if not is_exists(path):
        print('폴더가 존재하지 않습니다. (path : {})'.format(path))
        return False

    try:
        shutil.rmtree(path)
    except Exception as e:
        print(e)
        return False

    return True


def is_exists(path: str) -> bool:
    return os.path.exists(path)




if __name__ == '__main__':
    print(generate_key('test'))
    print(get_dir_name(generate_key('test'), 'testData'))
    print(is_exists(get_path('/root/anaconda3/envs/voicestudio2.0', 'test1', 'test2')))
