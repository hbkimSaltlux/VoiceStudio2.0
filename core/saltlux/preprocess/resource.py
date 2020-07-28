

class TestResource():
    def __init__(self):
        self.temp = []


    def add(self, key):
        self.temp.append(key)


    def show(self):
        print(self.temp)