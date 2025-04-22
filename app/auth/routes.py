from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, UserRoles, Family, FamilyMembers
import uuid
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
        return redirect(url_for('main.index'))
    
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

        # Check if the user wants to create or join a family
        create_or_join = form.create_or_join.data
        if create_or_join == 'create':
            family_name = form.family_name.data
            new_family = Family(name=family_name, owner_id=user.id)  # Automatically generates invitation_code
            db.session.add(new_family)
            db.session.commit()

            family_member = FamilyMembers(user_id=user.id, family_id=new_family.id, role_in_family='owner')
            db.session.add(family_member)
            db.session.commit()

            flash(f"Family '{family_name}' created successfully! Share this invitation code: {new_family.invitation_code}", 'info')
            

        elif create_or_join == 'join':
            invitation_code = form.invitation_code.data
            family = Family.query.filter_by(invitation_code=invitation_code).first()
            if family:
                family_member = FamilyMembers(user_id=user.id, family_id=family.id)
                db.session.add(family_member)
                db.session.commit()
                flash(f"You have successfully joined the '{family.name}' family!", 'info')
            else:
                flash("Invalid invitation code.", 'warning')

        db.session.commit() # Commit the user role and family association
        login_user(user)

        return redirect(url_for('main.dashboard'))
    
    return render_template('auth/register.html', 
                           title='Register', 
                           form=form)