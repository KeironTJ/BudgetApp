from app.vehicle import bp
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.models import VehicleData
from app import db
from app.vehicle.forms import VehicleDataForm

### VEHICLES
@bp.route('/vehicle_home')
@login_required
def vehicle_home():

    user_vehicles = db.session.query(VehicleData)

    return render_template("vehicle/vehicle_home.html", 
                           title="Vehicle Home",
                           user_vehicles = user_vehicles)


@bp.route('/vehicle_add_vehicle',methods=['GET', 'POST'])
@login_required
def vehicle_add_vehicle():

    vehicle_data_form = VehicleDataForm()

    if request.method == 'POST' and vehicle_data_form.validate():
        vehicle_data = VehicleData(user_id = current_user.id,
                                   vehicle_nickname = vehicle_data_form.vehicle_nickname.data,
                                   vrn = vehicle_data_form.vrn.data,
                                   vehicle_make = vehicle_data_form.vehicle_make.data,
                                   vehicle_model = vehicle_data_form.vehicle_model.data,
                                   vehicle_fuel_tank_size = vehicle_data_form.vehicle_fuel_tank_size.data,
                                   vehicle_fuel_type = vehicle_data_form.vehicle_fuel_type.data,
                                   vehicle_active = True)
        
        db.session.add(vehicle_data)
        db.session.commit()
        flash("Vehicle added!")
        return redirect(url_for('vehicle.vehicle_home'))


    return render_template("vehicle/vehicle_add_vehicle.html", 
                           title="Add Vehicle",
                           vehicle_data_form = vehicle_data_form )


## FUEL LOGS
@bp.route('/fuel_log_add_entry')
@login_required
def fuel_log_add_entry():

    return render_template("vehicle/fuel_log_add_entry.html", title="Add Fuel Log Entry")


@bp.route('/fuel_log_view_entries')
@login_required
def fuel_log_view_entries():

    return render_template("vehicle/fuel_log_view_entries.html", title="View Fuel Log")