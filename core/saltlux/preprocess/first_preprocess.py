

class FirstPreprocess():
    def __init__(self, resource):
        self.resource = resource
        print('init first Proc')

    def __call__(self, param):
        input_json = param
        print(input_json)
        self.resource.add('first')
        self.resource.show()
        return {'result': 'first hello'}
