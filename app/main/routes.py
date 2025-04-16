from app.main import bp
from flask import render_template
from flask_login import login_required, current_user
from app import db, socketio
from datetime import datetime, timedelta

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('main/index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('main/dashboard.html')





