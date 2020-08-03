from core.saltlux.preprocess import Prepare
from core.saltlux.resource import CommonResource, DataResource, PreprocessResource


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

    common_resource = CommonResource()

    data_dir = common_resource.data_dir
    preprocess_dir = common_resource.preprocess_dir
    preprocess_config = common_resource.preprocess_config

    data_resource = DataResource(data_dir)
    preprocess_resource = PreprocessResource(preprocess_dir, preprocess_config)

    restfuls['/preprocess/prepare'] = Prepare(data_resource=data_resource, preprocess_resource=preprocess_resource)

    return restfuls