# create imports
from app import db
from app.models import User, Role, UserRoles, MealPlan, Message, Family, FamilyMembers
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import login_required, current_user 
from app.admin.decorators import admin_required
from app.admin import bp
from app.admin.forms import AddMealForm, AssignRoleForm


## Admin Routes
# Displays the admin home page
@bp.route('/admin_home', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home():

    return render_template('admin/admin_home.html',
                           title='Admin Home')

# Displays the error page when a user is not an admin
@bp.route('/not_admin')
def not_admin():
    return render_template('admin/not_admin.html', title='Not Admin')


# Displays all user information
@bp.route('/admin_users', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():
    assignuserroleform = AssignRoleForm()

    users = db.session.query(User).all()
    roles = db.session.query(Role).all()
    user_roles = db.session.query(UserRoles).all()

    if assignuserroleform.validate_on_submit():
        user = db.session.query(User).filter_by(username=assignuserroleform.username.data).first()
        
        if "assign" in request.form:  # Check which button was clicked
            if user and user.assign_user_role(assignuserroleform.role.data):
                db.session.commit()
                flash('Role assigned successfully!', 'success')
            else:
                flash('Invalid user or role.', 'danger')

        elif "unassign" in request.form:  # Check if "Unassign" was clicked
            if user and user.unassign_user_role(assignuserroleform.role.data):
                db.session.commit()

                # Refresh the user_roles query after deletion
                user_roles = db.session.query(UserRoles).all()

                flash('Role unassigned successfully!', 'success')
            else:
                flash('Invalid user or role.', 'danger')


    return render_template('admin/admin_users.html',
                           title='Admin Users',
                           users=users,
                           roles=roles,
                           user_roles=user_roles,
                           assignuserroleform=assignuserroleform)

##Messages
# Displays the admin messages page
@bp.route('/admin_messages', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_messages():

    messages = db.session.query(Message).all()

    return render_template('admin/admin_messages.html', 
                           title='Admin Messages',
                           messages=messages)


## MealPlanner
# Displays the admin mealplanner page
@bp.route('/admin_mealplanner', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_mealplanner():    

    form = AddMealForm()
    mealplan = MealPlan.query.all()

    return render_template('admin/admin_mealplanner.html',
                           title='Admin Meal Planner',
                           mealplan=mealplan, 
                           form=form)

@bp.route('/admin_add_meal', methods=['GET', 'POST'])
def add_meal():
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
        return redirect(url_for('admin.admin_mealplanner'))
    elif request.method == 'POST':
        flash('Please fill in all fields.', 'danger')

    return redirect(url_for('admin.admin_mealplanner'))

@bp.route('/admin_edit_meal/<int:meal_id>', methods=['GET', 'POST'])
def edit_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    form = AddMealForm()
    if form.validate_on_submit():
        meal.meal_date = form.meal_date.data
        meal.meal_description = form.meal_description.data
        meal.meal_source = form.meal_source.data
        db.session.commit()
        flash("Meal updated successfully!", "success")
    return redirect(url_for('admin.admin_mealplanner'))

@bp.route('/admin_delete_meal/<int:meal_id>', methods=['POST'])
def delete_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    flash("Meal deleted successfully!", "success")
    return redirect(url_for('admin.admin_mealplanner'))
    

## FAMILIES
@bp.route('/admin_families', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_families():
    users = db.session.query(User).all()
    families = db.session.query(Family).all()
    family_members = db.session.query(FamilyMembers).all()

    return render_template('admin/admin_families.html',
                           title='Admin Families',
                           users=users,
                           families=families,
                           family_members=family_members)