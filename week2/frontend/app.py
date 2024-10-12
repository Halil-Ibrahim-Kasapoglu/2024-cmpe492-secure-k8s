from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend-service:5000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-random', methods=['GET'])
def get_random():
    response = requests.get(f"{BACKEND_URL}/random")
    print(f"Response from backend: {response.status_code}, {response.text}")
    if response.status_code != 200:
        return 'Error: {}'.format(response.text)
    return response.json()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
