from flask_socketio import emit
from app import socketio, db
from app.models import Message, User

@socketio.on('connect')
def handle_connect():
    print("Client connected successfully!")
    emit('server_message', {'data': 'Welcome! WebSocket connected.'}, broadcast=True)
    
    
@socketio.on('new_message')
def handle_new_message(data):
    user = User.query.get(data["user_id"])  # Fetch the user
    if not user:
        return  # Prevent issues with missing usernames

    message = Message(user_id=user.id, content=data["content"])
    db.session.add(message)
    db.session.commit()

    emit('message_received', {
        'id': message.id,
        'user_id': message.user_id,  # Ensure this is sent
        'username': user.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }, broadcast=True)

@socketio.on('delete_message')
def handle_delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        message.deleted = True
        db.session.commit()

        emit('message_deleted', {
            'message_id': message.id,
            'timestamp': message.timestamp.strftime("%d-%m-%Y %H:%M:%S")  # 🔹 Ensure WebSocket sends timestamp
        }, broadcast=True)

