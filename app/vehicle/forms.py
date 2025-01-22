from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError 
from app import db
import sqlalchemy as sa 
from app.models import User, VehicleData, FuelEntryLog


class AddVehicleDataForm(FlaskForm):
    vehicle_nickname = StringField('Vehicle Nickname', validators=[DataRequired()])
    vrn = StringField('Vehicle Registration Number', validators=[DataRequired()])
    vehicle_make = StringField('Make')
    vehicle_model = StringField('Model')
    vehicle_fuel_tank_size = IntegerField('Fuel Tank Size (Gallons)', validators=[DataRequired()])
    vehicle_fuel_type = StringField('Fuel Type')
    vehicle_active = BooleanField('Active?', validators=[DataRequired()])
    submit = SubmitField('Add Vehicle')


class AddFuelDataForm(FlaskForm):
    vehicle_nickname = StringField('Vehicle Nickname', validators=[DataRequired()]) #TODO: Make This a selection field
    entry_date = DateField('Date of Fueling', validators=[DataRequired()])
    fuel_price = IntegerField('Fuel Price', validators=[DataRequired()])
    vehicle_mileage = IntegerField('Mileage', validators=[DataRequired()])
    fuel_cost = IntegerField('Fuel Cost', validators=[DataRequired()])
    submit = SubmitField('Add Fuel Entry')
