from app.main import bp
from flask import render_template, request, redirect, url_for
from app import db
from app.models import Message
from app.main.forms import MessageForm
from flask_login import login_required, current_user

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm()
    if form.validate_on_submit():
        # Save the message
        new_message = Message(
            user_id=current_user.id,  # Use the logged-in user's ID
            content=form.content.data
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('main.index'))  # Reload the page after submission

    # Add pagination
    page = request.args.get('page', 1, type=int)  # Get the current page from query parameters
    messages_paginated = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=5)

    # `messages_paginated.items` will have access to `message.user.username` through the relationship
    return render_template(
        'main/index.html',
        form=form,
        messages=messages_paginated.items,  # Current page's messages
        pagination=messages_paginated  # Pagination object
    )