from flask import Flask, request
from core.saltlux import SaltluxSttCore

app = Flask(__name__)

saltluxSttRestful = SaltluxSttCore()

@app.route('/preprocess/first', methods=['POST'])
def preprocess_first():
    param = request.get_json()
    return saltluxSttRestful('/preprocess/first', param)

@app.route('/preprocess/dummy/second', methods=['POST'])
def preprocess_second():
    param = request.get_json()
    return saltluxSttRestful('/preprocess/dummy/second', param)

@app.route('/train/start', methods=['POST'])
def train_start():
    param = request.get_json()
    return saltluxSttRestful('/train/start', param)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6666, threaded=True, debug=True)