import pika
import requests
import json

from blender import update_blender_file

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='render_queue')


def callback(ch, method, properties, body):
    try:
        bodyJSON  = json.loads(body)
        
        status = update_blender_file(f"./{bodyJSON.get('session_id', 'untitled')}.blend", bodyJSON.get('points', []))
        
        if status == 0:
            print('Success! Points added.')
            ch.basic_ack(delivery_tag=method.delivery_tag)
        elif status == -1:
            notify_server_failure('File not found. Could not create new file.')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        elif status == -2:
            notify_server_failure('Mesh updation error.')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)           
        elif status == -3:
            notify_server_failure('File save error.')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)          

    except Exception as e:
        print(f"Error occurred during file processing: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def notify_server_failure(message):
    server_url = 'http://localhost:5000/notify_failure'
    payload = {'message': message}
    try:
        response = requests.post(server_url, json=payload)
        if response.status_code == 200:
            print("Notification sent to the server")
        else:
            print(f"Failed to send notification. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")


if __name__ == '__main__':
    channel.basic_consume(queue='render_queue', on_message_callback=callback, auto_ack=False)

    print('Receiver is waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
