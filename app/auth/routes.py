from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, UserRoles, Family, FamilyMembers
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user 
import sqlalchemy as sa 
from urllib.parse import urlsplit
from app.auth import bp
from app.family_manager.helper import create_or_join_family

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
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        # Assign the user to the default role (user)
        user_role = UserRoles(user_id=user.id, role_id=2)
        db.session.add(user_role)
        db.session.commit()
        flash('You have been assigned the default user role.')

        # Handle family creation or joining
        create_or_join = form.create_or_join.data
        family_name = form.family_name.data if create_or_join == 'create' else None
        invitation_code = form.invitation_code.data if create_or_join == 'join' else None

        if create_or_join_family(user, create_or_join, family_name, invitation_code):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        # If family creation/joining fails, redirect back to registration
        return redirect(url_for('auth.register'))

    return render_template('auth/register.html', 
                           title='Register', 
                           form=form)