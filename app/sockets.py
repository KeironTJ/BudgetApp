from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print("Client connected successfully!")
    emit('server_message', {'data': 'Welcome! WebSocket connected.'}, broadcast=True)
    

@socketio.on('new_message', namespace='/main')
def handle_new_message(data):
    print(f"Received message: {data}")
    emit('new_message', data, namespace='/main', broadcast=True)
