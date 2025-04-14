from app.main import bp
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import Message, MealPlan, ActivityPlan
from app.main.forms import AddMealForm, MessageForm, AddActivityForm
from flask_login import login_required, current_user
from app import db, socketio
from datetime import datetime, timedelta

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('main/index.html')


## Messaging Routes
@bp.route('/familychat', methods=['GET', 'POST'])
@login_required
def familychat():
    form = MessageForm()

    if form.validate_on_submit() and form.content.data.strip():

        return jsonify({'status': 'success'})

    # Load full message history **only on page load** (not during message sending)
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('main/familychat.html', 
                            title='Family Chat',
                            form=form,
                            messages=messages)

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

    
    addMealForm = AddMealForm()
    if addMealForm.validate_on_submit():
        meal = MealPlan(
            user_id=current_user.id,
            meal_title=addMealForm.meal_title.data,
            meal_date=addMealForm.meal_date.data,
            meal_description=addMealForm.meal_description.data,
            meal_source=addMealForm.meal_source.data
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
                           addMealForm=addMealForm)

@bp.route('/meal_details/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def meal_details(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    editmealform = AddMealForm(obj=meal)

    if editmealform.validate_on_submit():
        editmealform.populate_obj(meal)
        db.session.commit()
        flash("Meal updated successfully!", "success")
        return redirect(url_for('main.mealplanner'))

    return render_template('main/meal_details.html', 
                           title='Meal Details',
                           editmealform=editmealform,
                           meal=meal)



@bp.route('/delete_meal/<int:meal_id>', methods=['GET','POST'])
def delete_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    flash("Meal deleted successfully!", "success")
    return redirect(url_for('main.mealplanner'))

## Family Activity Planner Routes
@bp.route('/activityplanner', methods=['GET', 'POST'])
@login_required
def activityplanner():
    addactivityform = AddActivityForm()
    activities = ActivityPlan.query.order_by(ActivityPlan.activity_start_date.asc(),
                                             ActivityPlan.activity_start_time.asc()
                                             ).all()

    if addactivityform.validate_on_submit():

        activity = ActivityPlan(
            user_id=current_user.id,
            activity_start_date=addactivityform.activity_start_date.data,
            activity_end_date=addactivityform.activity_end_date.data,
            activity_start_time=addactivityform.activity_start_time.data,
            activity_end_time=addactivityform.activity_end_time.data,
            activity_all_day_event=addactivityform.activity_all_day_event.data,
            activity_title=addactivityform.activity_title.data,
            activity_description=addactivityform.activity_description.data,
            activity_comments=addactivityform.activity_comments.data,
            activity_location=addactivityform.activity_location.data
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added successfully!', 'success')
        return redirect(url_for('main.activityplanner'))


    return render_template('main/activityplanner.html',
                           title='Activity Planner',
                           activities=activities,
                           addactivityform=addactivityform)


@bp.route('/activity_details/<int:id>', methods=['GET', 'POST'])
@login_required
def activity_details(id):

    activity = ActivityPlan.query.get_or_404(id)
    editactivityform = AddActivityForm(obj=activity)

    if editactivityform.validate_on_submit():
        editactivityform.populate_obj(activity)
        db.session.commit()
        flash("Activity updated successfully!", "success")
        return redirect(url_for('main.activity_details', id=activity.id))
    
    return render_template("main/activity_details.html", 
                           editactivityform=editactivityform, 
                           activity=activity)


@bp.route('/delete_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_activity(id):
    activity = ActivityPlan.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted successfully!", "danger")
    return redirect(url_for('main.activityplanner'))

