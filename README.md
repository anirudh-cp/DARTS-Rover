# DARTS Rover Dashboard

Control panel dashboard for the Deep Adventurer for Rapid Survey and Exploration Rover.

### Local Setup and Run:

- Install RabbitMQ and start the server.
- Python requirement setup:

        pip install -r requirements.txt


- For running the flask server:

        python wsgi.py
        
- For running the 3D point processing:

        cd render_process
        python interface.py
    

### API Endpoint:

- Send a set of points via a POST request under the key 'points' with the session ID in the path.

        POST /api/send/{session_id}