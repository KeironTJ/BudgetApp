from app.main import bp
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import Message, MealPlan
from app.main.forms import AddMealForm
from app.main.forms import MessageForm
from flask_login import login_required, current_user
from flask_socketio import emit
from app import db, socketio
from datetime import datetime, timedelta

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm()

    if form.validate_on_submit() and form.content.data.strip():

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

    return jsonify([{ 
        'id': msg.id, 
        'deleted': msg.deleted,
        'username': msg.user.username, 
        'content': msg.content if not msg.deleted else None, 
        'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for msg in messages])


@bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    # Ensure only the message owner or admin can delete
    if message.user_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403

    message.deleted = True
    db.session.commit()

    # Emit WebSocket event ONLY after successful deletion
    socketio.emit('message_deleted', {
        'message_id': message.id,
        'username': message.user.username,
        'timestamp': message.timestamp.strftime("%d-%m-%Y %H:%M:%S")
    })

    return jsonify({'status': 'success'})


## Meal Planner Routes
@bp.route('/mealplanner', methods=['GET', 'POST'])
@login_required
def mealplanner():
    # Get today's date
    today = datetime.today()
    
    # Calculate the Monday of the current week
    start_of_week = today - timedelta(days=today.weekday())  # Monday is weekday 0

    # Filter meals including Monday
    mealplan = MealPlan.query.filter(MealPlan.meal_date >= start_of_week.date()) \
                         .order_by(MealPlan.meal_date.asc()) \
                         .all()

    
    form = AddMealForm()
    if form.validate_on_submit():
        meal = MealPlan(
            user_id=current_user.id,
            meal_date=form.meal_date.data,
            meal_description=form.meal_description.data,
            meal_source=form.meal_source.data
        )
        db.session.add(meal)
        db.session.commit()
        flash('Meal added successfully!', 'success')
        return redirect(url_for('main.mealplanner'))
    elif request.method == 'POST':
        flash('Please fill in all fields.', 'danger')

    return render_template('main/mealplanner.html',
                           title='Meal Planner',
                           mealplan=mealplan,
                           form=form)

@bp.route('/edit_meal/<int:meal_id>', methods=['GET', 'POST'])
def edit_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    form = AddMealForm()
    if form.validate_on_submit():
        meal.meal_date = form.meal_date.data
        meal.meal_description = form.meal_description.data
        meal.meal_source = form.meal_source.data
        db.session.commit()
        flash("Meal updated successfully!", "success")
    return redirect(url_for('main.mealplanner'))


@bp.route('/delete_meal/<int:meal_id>', methods=['POST'])
def delete_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    flash("Meal deleted successfully!", "success")
    return redirect(url_for('main.mealplanner'))