from app.family_manager import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from datetime import datetime, timedelta
from app.models import User, Family, FamilyMembers
from sqlalchemy.orm import joinedload

@bp.route('/family_home/<family_name>', methods=['GET', 'POST'])
@login_required
def family_home(family_name):
    family = Family.query.filter_by(name=family_name).options(joinedload(Family.members)).first_or_404()
    if not family:
        flash('Family not found.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('family_manager/family_home.html',
                           family=family,
                           family_name=family_name,
                           title='Family Home')


