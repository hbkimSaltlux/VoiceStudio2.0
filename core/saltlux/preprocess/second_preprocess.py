

class SecondPreprocess():
    def __init__(self, resource):
        self.resource = resource
        print('init second Proc')

    def __call__(self, param):
        input_json = param
        print(input_json)
        self.resource.add('second')
        self.resource.show()
        return {'result': 'second hello'}
