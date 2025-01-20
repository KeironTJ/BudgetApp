from app.vehicle import bp
from flask import render_template
from flask_login import login_required 

### VEHICLES
@bp.route('/vehicle_home')
@login_required
def vehicle_home():

    return render_template("vehicle/vehicle_home.html", title="Vehicle Home")


@bp.route('/vehicle_add_vehicle')
@login_required
def vehicle_add_vehicle():

    return render_template("vehicle/vehicle_add_vehicle.html", title="Add Vehicle")


## FUEL LOGS
@bp.route('/fuel_log_add_entry')
@login_required
def fuel_log_add_entry():

    return render_template("vehicle/fuel_log_add_entry.html", title="Add Fuel Log Entry")


@bp.route('/fuel_log_view_entries')
@login_required
def fuel_log_view_entries():

    return render_template("vehicle/fuel_log_view_entries.html", title="View Fuel Log")