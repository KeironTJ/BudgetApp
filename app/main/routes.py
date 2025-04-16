from app.main import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, socketio
from datetime import datetime, timedelta
from app.models import User
from app.main.forms import EditProfileForm

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('main/index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('main/dashboard.html')


@bp.route('/user_profile/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):

    user = User.query.filter_by(username=username).first()
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.user_profile', username=user.username))

    if not user:
        return render_template('main/404.html'), 404

    return render_template('main/user_profile.html', 
                           user=user,
                           form=form)






