from flask import Flask, jsonify, render_template, request
import requests
import time

app = Flask(__name__)

# Define the API URL from the server Tornado
API_URL = 'http://localhost:8000/api'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    channel = request.args.get('channel', 'wavelengths')  # Default to wavelengths
    index = int(request.args.get('index', 0))  # Default to the first entry (0-based index)

    # Fetch data from the API
    response = requests.get(API_URL)
    data = response.json()

    value = data[channel][index]

    return jsonify({'value': value, 'timestamp': time.time()})

if __name__ == '__main__':
    app.run(debug=True)
