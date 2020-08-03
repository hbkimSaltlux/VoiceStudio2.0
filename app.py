from flask import Flask, request
from core.saltlux import SaltluxSttCore

app = Flask(__name__)

saltluxSttRestful = SaltluxSttCore()

@app.route('/preprocess/prepare', methods=['POST'])
def preprocess_first():
    param = request.get_json()
    return saltluxSttRestful('/preprocess/prepare', param)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666, threaded=True, debug=True)