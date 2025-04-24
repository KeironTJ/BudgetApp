from app.meal_planner import bp
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.models import  MealPlan
from app.meal_planner.forms import AddMealForm
from flask_login import login_required, current_user
from app import db
from datetime import datetime, timedelta
from app.decorators import active_family_required


## Meal Planner Routes
@bp.route('/mealplanner', methods=['GET', 'POST'])
@login_required
@active_family_required
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
        return redirect(url_for('meal_planner.mealplanner'))
    
    elif request.method == 'POST':
        flash('Please fill in all fields.', 'danger')

    return render_template('meal_planner/mealplanner.html',
                           title='Meal Planner',
                           mealplan=mealplan,
                           addMealForm=addMealForm)

@bp.route('/meal_details/<int:meal_id>', methods=['GET', 'POST'])
@login_required
@active_family_required
def meal_details(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    editmealform = AddMealForm(obj=meal)

    if editmealform.validate_on_submit():
        editmealform.populate_obj(meal)
        db.session.commit()
        flash("Meal updated successfully!", "success")
        return redirect(url_for('meal_planner.mealplanner'))

    return render_template('meal_planner/meal_details.html', 
                           title='Meal Details',
                           editmealform=editmealform,
                           meal=meal)



@bp.route('/delete_meal/<int:meal_id>', methods=['GET','POST'])
def delete_meal(meal_id):
    meal = MealPlan.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    flash("Meal deleted successfully!", "success")
    return redirect(url_for('meal_planner.mealplanner'))



