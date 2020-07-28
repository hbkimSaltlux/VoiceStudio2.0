from core.saltlux.preprocess import FirstPreprocess, SecondPreprocess, TestResource
from core.saltlux.train import TransferLearning


class SaltluxSttCore():
    def __init__(self):
        self.restfuls = _get_available_restfuls()

    def __call__(self, api_name, params):
        is_available = self._is_available_restful(api_name)
        if is_available:
            api = self.restfuls[api_name]
            return api(params)

        else:
            return {'result': None, 'errorCode': 100, 'errorMessage': '{} 은 지원하지 않는 기능 입니다.'.format(api_name)}

    def _is_available_restful(self, api_name):
        if api_name in self.restfuls.keys():
            return True

        else:
            return False


def _get_available_restfuls():
    restfuls = {}

    testResource = TestResource()

    restfuls['/preprocess/first'] = FirstPreprocess(testResource)
    restfuls['/preprocess/dummy/second'] = SecondPreprocess(testResource)
    restfuls['/train/start'] = TransferLearning(testResource)

    return restfuls