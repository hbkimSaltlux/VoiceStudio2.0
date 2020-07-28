

class TransferLearning():
    def __init__(self, resource):
        self.resource = resource
        print('init transfer learning')

    def __call__(self, param):
        input_json = param
        print(input_json)
        self.resource.add('transfer')
        self.resource.show()
        return {'result': 'transfer hello'}
