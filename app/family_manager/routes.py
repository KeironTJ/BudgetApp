from app.family_manager import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from datetime import datetime, timedelta
from app.models import User, Family, FamilyMembers
from app.family_manager.forms import FamilySelectForm, FamilyCreateorJoinForm
from sqlalchemy.orm import joinedload
from app.decorators import active_family_required
from app.family_manager.helper import create_or_join_family

@bp.route('/family_home/<family_name>', methods=['GET', 'POST'])
@login_required
@active_family_required
def family_home(family_name):
    family = Family.query.filter_by(name=family_name).options(joinedload(Family.members)).first_or_404()
    if not family:
        flash('Family not found.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('family_manager/family_home.html',
                           family=family,
                           family_name=family_name,
                           title='Family Home')

@bp.route('/family_choose', methods=['GET', 'POST'])
@login_required
def family_choose():
    form = FamilySelectForm()
    form.family.choices = [(family.id, family.name) for family in current_user.families]

    if form.validate_on_submit():
        # Set the selected family as the active family
        family_id = form.family.data

        if current_user.set_active_family(family_id):
            db.session.commit()
            flash("Active family updated successfully.", "success")

        else:
            flash("Failed to update active family.", "danger")
        return redirect(url_for('main.dashboard'))


    return render_template('family_manager/family_choose.html',
                           title='Choose Family',
                           form=form)   

@bp.route('/create_or_join_family_view', methods=['GET', 'POST'])
@login_required
def create_or_join_family_view():
    form = FamilyCreateorJoinForm()  # You can reuse or create a new form for this purpose

    if form.validate_on_submit():

        # Handle family creation or joining
        create_or_join = form.create_or_join.data
        family_name = form.family_name.data if create_or_join == 'create' else None
        invitation_code = form.invitation_code.data if create_or_join == 'join' else None

        if create_or_join_family(current_user, create_or_join, family_name, invitation_code):
            return redirect(url_for('main.dashboard'))

    return render_template('family_manager/create_or_join_family_view.html', 
                           title='Create or Join Family', 
                           form=form)