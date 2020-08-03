

class CustomError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def get_code(self) -> int:
        return self.code

    def get_message(self) -> str:
        return self.message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    try:
        raise CustomError(500, 'custom error')
    except Exception as e:
        print({"result": None, "errCode": e.get_code(),"errMessage": e.get_message()})