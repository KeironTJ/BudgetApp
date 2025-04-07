from flask_socketio import emit
from app import socketio, db
from app.models import Message, User

@socketio.on('connect')
def handle_connect():
    print("Client connected successfully!")
    emit('server_message', {'data': 'Welcome! WebSocket connected.'}, broadcast=True)
    
    
@socketio.on('new_message')
def handle_new_message(data):
    user = User.query.get(data["user_id"])  
    if not user:
        return  # Prevent issues with missing usernames

    message = Message(user_id=user.id, content=data["content"])
    db.session.add(message)
    db.session.commit()

    emit('message_received', {
        'id': message.id,
        'user_id': message.user_id, 
        'username': user.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime("%d-%m-%Y %H:%M:%S")
    }, broadcast=True)

@socketio.on("delete_message")
def handle_delete_message(data):
    print(f"Received WebSocket delete request: {data}")  # Debugging log

    message_id = data.get("message_id")
    if not message_id:
        print("Error: No message_id received in WebSocket event")  # Debug log
        return

    message = Message.query.get(message_id)
    if not message:
        print(f"Error: Message ID {message_id} not found in DB!")  # Debug log
        return

    message.deleted = True
    db.session.commit()

    print(f"Emitting WebSocket event for message_id: {message_id}")  # Debug log
    emit("message_deleted", {
        "message_id": message_id,
        "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "username": message.user.username,
    }, broadcast=True)