from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
import logging
import json

import socket
host_addr = socket.gethostbyname(socket.gethostname())
print(host_addr)

app = Flask(__name__)
CORS(app)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='render_queue')

logging.basicConfig(level=logging.INFO,
                    # filename='app.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@app.route('/api/send/<session_id>', methods=['POST', ])
def send_data(session_id):

    s = request.get_data()
    s = s.decode('utf-8')
    print(s)
    input = s.split(',')
    print(input)
    l = []

    for i in range(0, len(input), 3):
        l.append([float(input[i]), float(input[i+1]), float(input[i+2])])
    print(l)
    points = l
    print(points)

    try:
        channel.basic_publish(exchange='',
                              routing_key='render_queue',
                              body=json.dumps({'session_id': session_id, 'points': points}))
        return jsonify({'message': 'Message sent to RabbitMQ'})
    except pika.exceptions.AMQPError as e:
        # Handle AMQP exceptions
        return jsonify({'error': f'Error in sending message: {e}'})


@app.route('/notify_failure', methods=['POST', ])
def notify_failure():
    data = request.get_json()
    message = data.get('message')
    logging.error(f'File processing failed: {message}')
    return jsonify({'message': 'Failure notification received'})