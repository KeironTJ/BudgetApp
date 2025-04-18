from app.vehicle import bp
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app.models import VehicleData, FuelEntryLog
from app import db
from app.vehicle.forms import AddVehicleDataForm, AddFuelDataForm
from decimal import Decimal

### VEHICLES
@bp.route('/vehicle_home')
@login_required
def vehicle_home():

    return render_template("vehicle/vehicle_home.html", 
                           title="Vehicle Home")

@bp.route('/vehicle_view_vehicle', methods=['GET', 'POST'])
@login_required
def vehicle_view_vehicle():

    user_vehicles = db.session.query(VehicleData).filter_by(user_id=current_user.id).all()

    return render_template("vehicle/vehicle_view_vehicle.html", 
                           title="View Vehicle",
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
    current_user_id = current_user.id

    add_fuel_data_form = AddFuelDataForm()

    # List for SelectField to vrn choices
    vehicles = VehicleData.query.filter_by(user_id=current_user_id).all()
    add_fuel_data_form.vehicle_nickname.choices = [(vehicle.vehicle_nickname, vehicle.vehicle_nickname) for vehicle in vehicles]


    if request.method == 'POST' and add_fuel_data_form.validate():
        fuel_data = FuelEntryLog(
            user_id=current_user.id,
            vrn=add_fuel_data_form.vehicle_nickname.data,  # TODO: CHANGE TO SELECT vrn via nickname
            entry_date=add_fuel_data_form.entry_date.data,
            fuel_price=float(add_fuel_data_form.fuel_price.data),
            vehicle_mileage=add_fuel_data_form.vehicle_mileage.data,
            fuel_cost=float(add_fuel_data_form.fuel_cost.data)
        )
        
        # Calculate additional fields
        fuel_data.calculateActualMiles()
        fuel_data.calculateLitre()
        fuel_data.calculateGallon()
        fuel_data.calculateMPG()

        # Convert Decimal fields to float before committing to the database
        fuel_data.litres = float(fuel_data.litres)
        fuel_data.gallon = float(fuel_data.gallon)
        fuel_data.mpg = float(fuel_data.mpg)

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

@bp.route('/delete-entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = FuelEntryLog.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry Deleted")
    return redirect(url_for('vehicle.fuel_log_view_entries'))


@bp.route('/journey_add_entry', methods=['GET', 'POST'])
@login_required
def journey_add_entry():


    return render_template("vehicle/journey_add_entry.html", 
                           title="Add Journey Entry")

@bp.route('/journey_view_log', methods=['GET', 'POST'])
@login_required
def journey_view_log():

    return render_template("vehicle/journey_view_log.html", 
                           title="View Journey Log")