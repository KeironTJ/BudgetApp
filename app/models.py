from sqlalchemy import Integer, String, func, DateTime, Time, Boolean
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

    first_name = db.Column(String(64), nullable=True)  
    last_name = db.Column(String(64), nullable=True)  
    primary_phone_number = db.Column(String(20), nullable=True) 
    secondary_phone_number = db.Column(String(20), nullable=True)  
    dob = db.Column(DateTime, nullable=True)
    profile_picture = db.Column(String(256), nullable=True)  #TODO: Add URL or path to the profile picture 


    #Relationships
    roles = so.relationship('Role', secondary='user_roles', back_populates='users')
    address = so.relationship('Address', back_populates='user', uselist=False)  # One-to-one relationship with Address
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return 'admin' in [role.name for role in self.roles]
    
    def is_family_leader(self):
        return 'family_leader' in [role.name for role in self.roles]
    
    def is_family_member(self):
        return 'family_member' in [role.name for role in self.roles]
    
    def assign_user_role(self, role_name):
        role = db.session.query(Role).filter_by(name=role_name).first()
        if role and role not in self.roles:
            self.roles.append(role)
            return True 
        return False
    
    def unassign_user_role(self, role_name):
        role = db.session.query(Role).filter_by(name=role_name).first()
        if role and role in self.roles:
            self.roles.remove(role)  
            return True
        return False
    
# Model for addresses
class Address(db.Model):
    id = db.Column(Integer, primary_key=True)
    street_address = db.Column(String(255))
    city = db.Column(String(100))
    county = db.Column(String(100), nullable=True)  # Optional field
    postal_code = db.Column(String(20))
    country = db.Column(String(100), default='United Kingdom')  # Example default

    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    user = so.relationship("User", back_populates="address")

    def __repr__(self):
        return f'<Address: {self.street_address}, {self.city}, {self.postal_code}>'
    


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
    role_id = db.Column(Integer, db.ForeignKey('role.id'), default=2)


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
    deleted = db.Column(db.Boolean, default=False) 
    
    # Relationships
    user = db.relationship('User', backref='messages', lazy=True)  # Relationship to fetch User data


## MEAL PLANNING    
class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # KEEP AS REFERENCE - MAY LINK TO A FAMILY ID IN THE FUTURE
    meal_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    meal_title = db.Column(db.String(64),default="", nullable=False)
    meal_description = db.Column(db.String(500)) 
    meal_source = db.Column(db.String(500)) 

    # Relationships
    user = db.relationship('User', backref='meal_plans', lazy=True) 


## ACTIVITY PLANNING
class ActivityPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # KEEP AS REFERENCE - MAY LINK TO A FAMILY ID IN THE FUTURE
    activity_date = db.Column(db.DateTime, default=func.now())
    activity_start_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    activity_end_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    activity_title = db.Column(db.String(64), nullable=False)
    activity_all_day_event = db.Column(db.Boolean, default=True)
    activity_start_time = db.Column(db.Time)
    activity_end_time = db.Column(db.Time)
    activity_description = db.Column(db.String(500)) 
    activity_location = db.Column(db.String(500)) 
    activity_comments = db.Column(db.String(500))

    # Relationships
    user = db.relationship('User', backref='activity_plans', lazy=True)