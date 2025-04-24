from functools import wraps
from flask import redirect, url_for, request, flash
from flask_login import current_user
from app.models import Role, UserRoles
from app import db
from sqlalchemy.exc import SQLAlchemyError 

def active_family_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.get_active_family():
            flash("Please select an active family to continue.", "warning")
            # Store the intended destination in the query string
            return redirect(url_for('family_manager.family_choose', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user has admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not user_has_admin(current_user.id):
            # Redirect to a page indicating the user is not an admin
            return redirect(url_for('admin.not_admin')) 
        return f(*args, **kwargs)
    return decorated_function


# Function to check if user has admin role
def user_has_admin(user_id):
    try:
        # Directly check if the user has an admin role to optimize performance
        admin_role_id = db.session.query(Role.id).filter_by(name='admin').scalar()
        user_is_admin = db.session.query(UserRoles).filter_by(user_id=user_id, role_id=admin_role_id).first() is not None
        return user_is_admin
    except SQLAlchemyError as e:
        
        print(f"Database error occurred: {e}")
        return False