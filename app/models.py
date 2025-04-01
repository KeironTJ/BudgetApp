from sqlalchemy import Integer, String, func
from datetime import datetime, timezone
import sqlalchemy.orm as so 
from flask_login import UserMixin 
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# Model for the User table
class User(UserMixin, db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(120), index=True, unique=True)
    password_hash = db.Column(String(256))

    #Relationships
    roles = so.relationship('Role', secondary='user_roles', back_populates='users')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return 'admin' in [role.name for role in self.roles]
    

# Model for the Role table
class Role(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), index=True, unique=True)

    # Relationships
    users = so.relationship('User', secondary='user_roles', back_populates='roles')
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)
    

# Model for the UserRoles table
class UserRoles(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    role_id = db.Column(Integer, db.ForeignKey('role.id'))

    # Relationships


## VEHICLES
# Model for vehicle information
class VehicleData(db.Model):
    id = db.Column(Integer, primary_key = True)
    user_id = db.Column(Integer, db.ForeignKey('user.id')) 
    vehicle_nickname = db.Column(db.String(64))
    vrn = db.Column(db.String(64))
    vehicle_make = db.Column(db.String(64))
    vehicle_model = db.Column(db.String(64))
    vehicle_fuel_tank_size = db.Column(db.Integer)
    vehicle_fuel_type = db.Column(db.String(64))
    vehicle_active = db.Column(db.Boolean, default=True)

    # Relationships
    
class FuelEntryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    entry_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    vrn = db.Column(db.String(64))  
    fuel_price = db.Column(db.Integer)
    vehicle_mileage = db.Column(db.Integer)
    fuel_cost = db.Column(db.Integer)
    actual_miles = db.Column(db.Integer)
    litres = db.Column(db.Integer)
    gallon = db.Column(db.Integer)
    mpg = db.Column(db.Integer)

    def calculatePricePerLitre(self):
        return self.fuel_price / 100
    
    def calculateLitre(self):
        self.litres = round(self.fuel_cost / self.calculatePricePerLitre(),2)
    
    def calculateGallon(self):
        gallonperlitre = 4.54609
        self.gallon = round(self.litres / gallonperlitre,2)

    def calculateActualMiles(self):
        previous_entry = FuelEntryLog.query.filter_by(vrn=self.vrn).order_by(FuelEntryLog.entry_date.desc()).first()
        if previous_entry:
            self.actual_miles = self.vehicle_mileage - previous_entry.vehicle_mileage
        else:
            self.actual_miles = 0

    def calculateMPG(self):
        self.calculateActualMiles()
        self.calculateGallon()
        self.mpg = round(self.actual_miles / self.gallon,2) if self.gallon else 0

## MESSAGING
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User table
    content = db.Column(db.String(500), nullable=False)  
    timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)

    user = db.relationship('User', backref='messages', lazy=True)  # Relationship to fetch User data