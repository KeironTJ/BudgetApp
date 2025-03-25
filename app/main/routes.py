from app.main import bp
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Message
from app.main.forms import MessageForm
from flask_login import login_required, current_user




@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm()

    if form.validate_on_submit() and form.content.data.strip():
        new_message = Message(
            user_id=current_user.id,
            content=form.content.data
        )
        db.session.add(new_message)
        db.session.commit()

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    messages_paginated = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=5)

    # If the current page is invalid (e.g., due to new message or deletion)
    if page > messages_paginated.pages and messages_paginated.pages > 0:
        page = messages_paginated.pages
        messages_paginated = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=5)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            'main/_messages.html',
            messages=messages_paginated.items,
            pagination=messages_paginated
        )

    return render_template(
        'main/index.html',
        form=form,
        messages=messages_paginated.items,
        pagination=messages_paginated
    )


@bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to delete this message.', 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(message)
    db.session.commit()

    # Pagination logic
    page = request.args.get('page', 1, type=int)
    messages_paginated = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=5)

    if page > messages_paginated.pages and messages_paginated.pages > 0:
        page = messages_paginated.pages
        messages_paginated = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=5)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            'main/_messages.html',
            messages=messages_paginated.items,
            pagination=messages_paginated
        )

    return redirect(url_for('main.index', page=page))