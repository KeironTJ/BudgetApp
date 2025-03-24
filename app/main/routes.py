from app.main import bp
from flask import render_template, request, jsonify
from app import db
from app.models import Message
from flask_login import login_required 

### The index view function
@bp.route('/')
@bp.route('/index')
@login_required
def index():

    return render_template("main/index.html", title="Home")

@bp.route('/send_message', methods=['POST'])
@login_required
def send_message():
     data = request.get_json()
     new_message = Message(user_id=data['user_id'], content=data['content'])
     db.session.add(new_message)
     db.session.commit()
     return jsonify({"status": "Message sent!"}), 201

@bp.route('/get_messages', methods=['GET'])
@login_required
def get_messages():
     messages = Message.query.order_by(Message.timestamp.desc()).all()
     return jsonify([{
         "user_id": message.user_id,
         "content": message.content,
         "timestamp": message.timestamp
     } for message in messages])