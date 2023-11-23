from flask import Flask, render_template, request
import requests
from flask_cors import CORS
import pika
import logging
import json

import socket
host_addr = socket.gethostbyname(socket.gethostname())


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "server root", 200

@app.route('/test', methods=['POST'])
def index_():
    data = request.get_data()
    print(data)
    return "hello", 200

@app.route('/send/<message>')
def send_message(message):
    # Assuming all devices are connected on the same network
    # Send an HTTP request to all devices on the network
    # Modify the IP range according to your network setup
    for i in range(1, 255):
        ip = f'192.168.1.{i}'  # Adjust the IP range as per your network
        url = f'http://{ip}:5000/receive'
        try:
            response = requests.post(url, data={'message': message})
            print(f"Sent message '{message}' to {url}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to {url}: {e}")
    
    return f"Broadcasted message: {message}"

@app.route('/receive', methods=['POST'])
def receive_message():
    message = request.form.get('message')
    print(f"Received message: {message}")
    # You can process the received message here as needed
    return "Message received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
