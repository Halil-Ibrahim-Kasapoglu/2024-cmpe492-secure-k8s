from flask import Flask, request, jsonify
import random
import time 

app = Flask(__name__)

@app.route('/random', methods=['GET'])
def __random():
    random.seed(time.time())
    return jsonify({'random': random.randint(0, 100)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
