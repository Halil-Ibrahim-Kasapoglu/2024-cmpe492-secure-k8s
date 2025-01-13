from flask import Flask, request, jsonify
import random
import time 
import os

app = Flask(__name__)

OUTPUT_DIR = '/data'
FILE = 'data.txt'

def write_to_file(data):
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Write the data to the file
    with open(f'{OUTPUT_DIR}/{FILE}', 'a') as f:
        f.write(f'{data}')

def get_data():
    # Check if the file exists
    # If it doesn't, return "No data available"
    if not os.path.exists(f'{OUTPUT_DIR}/{FILE}'):
        return "No data available"

    # Read the data from the file
    with open(f'{OUTPUT_DIR}/{FILE}', 'r') as f:
        return f.readlines()
    
@app.route('/echo', methods=['GET'])
def __random():
    random.seed(time.time())
    random_letter = random.choice('abcdefghijklmnopqrstuvwxyz ')
    write_to_file(random_letter)
    return jsonify({
        'message': 'Data written to file',
        'letter': random_letter,
        'data': get_data()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
