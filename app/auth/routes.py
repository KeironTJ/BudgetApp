from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, UserRoles
from flask import render_template, redirect, url_for, flash, request 
from flask_login import current_user, login_user, logout_user 
import sqlalchemy as sa 
from urllib.parse import urlsplit
from app.auth import bp

## Authentication Routes
### The login view function
@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', 
                           title='Sign In', 
                           form=form)


@bp.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        #obtain user id
        user = db.session.query(User).filter_by(username=form.username.data).first()

        # Assign the user to the default role (user)
        user_role = UserRoles(user_id=user.id, role_id=2)
        db.session.add(user_role)
        db.session.commit()
        flash('You have been assigned the default user role.')

        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/register.html', 
                           title='Register', 
                           form=form)