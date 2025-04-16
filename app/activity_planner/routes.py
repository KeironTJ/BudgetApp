from app.activity_planner import bp
from flask import render_template, redirect, url_for, flash
from app.models import ActivityPlan
from app.activity_planner.forms import AddActivityForm
from flask_login import login_required, current_user
from app import db

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
        return redirect(url_for('activity_planner.activityplanner'))


    return render_template('activity_planner/activityplanner.html',
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
        return redirect(url_for('activity_planner.activity_details', id=activity.id))
    
    return render_template("activity_planner/activity_details.html", 
                           editactivityform=editactivityform, 
                           activity=activity)


@bp.route('/delete_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_activity(id):
    activity = ActivityPlan.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted successfully!", "danger")
    return redirect(url_for('activity_planner.activityplanner'))