from app.vehicle import bp
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.models import VehicleData, FuelEntryLog
from app import db
from app.vehicle.forms import AddVehicleDataForm, AddFuelDataForm

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

    vehicle_data_form = AddVehicleDataForm()

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
@bp.route('/fuel_log_add_entry',methods=['GET', 'POST'])
@login_required
def fuel_log_add_entry():
    add_fuel_data_form = AddFuelDataForm()

    if request.method == 'POST' and add_fuel_data_form.validate():
        fuel_data = FuelEntryLog(user_id = current_user.id,
                                   vrn = add_fuel_data_form.vehicle_nickname.data, #TODO: CHANGE TO SELECT vrn via nickname
                                   entry_date = add_fuel_data_form.entry_date.data,
                                   fuel_price = add_fuel_data_form.fuel_price.data,
                                   vehicle_mileage = add_fuel_data_form.vehicle_mileage.data,
                                   fuel_cost = add_fuel_data_form.fuel_cost.data)
        
        fuel_data.calculateActualMiles(),
        fuel_data.calculateLitre(),
        fuel_data.calculateGallon(),
        fuel_data.calculateMPG()

        db.session.add(fuel_data)
        db.session.commit()
        flash("Fuel Entry added!")
        return redirect(url_for('vehicle.fuel_log_view_entries'))
    

    return render_template("vehicle/fuel_log_add_entry.html", 
                           title="Add Fuel Log Entry",
                           add_fuel_data_form=add_fuel_data_form)


@bp.route('/fuel_log_view_entries')
@login_required
def fuel_log_view_entries():

    fuel_log = db.session.query(FuelEntryLog)

    return render_template("vehicle/fuel_log_view_entries.html", 
                           title="View Fuel Log",
                           fuel_log=fuel_log)