from app.main import bp
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Message
from app.main.forms import MessageForm
from flask_login import login_required, current_user
from flask_socketio import emit
from app import db, socketio

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm()

    if form.validate_on_submit() and form.content.data.strip():
        # 🔹 DO NOT commit here—WebSocket already handles saving the message
        return jsonify({'status': 'success'})

    # Load full message history **only on page load** (not during message sending)
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('main/index.html', form=form, messages=messages)


@bp.route('/load_messages')
@login_required
def load_messages():
    last_message_id = request.args.get("last_message_id", type=int)
    if not last_message_id:
        return jsonify({'error': 'Invalid message ID'}), 400

    messages = Message.query.filter(Message.id < last_message_id).order_by(Message.timestamp.asc()).limit(10).all()

    print(f"Loading messages before ID: {last_message_id}")  # 🔹 Debug lazy loading messages

    return jsonify([{ 
        'id': msg.id, 
        'deleted': msg.deleted,  # 🔹 Confirm whether the message is marked as deleted
        'username': msg.user.username, 
        'content': msg.content if not msg.deleted else "🚫 Message deleted",
        'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for msg in messages])


@bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    message.deleted = True
    db.session.commit()
    
    socketio.emit('message_deleted', {
        'message_id': message.id,
        'timestamp': message.timestamp.strftime("%d-%m-%Y %H:%M:%S")
    }, to=None)

    return jsonify({'status': 'success', 'message_id': message.id})