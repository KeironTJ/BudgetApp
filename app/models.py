from sqlalchemy import Integer, String, func, DateTime, Time, Boolean
from datetime import datetime, timezone
import sqlalchemy.orm as so 
from flask_login import UserMixin 
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


## USER MANAGEMENT
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
    active_family_id = db.Column(Integer, db.ForeignKey('family.id'), nullable=True) 

    #Relationships
    roles = so.relationship('Role', secondary='user_roles', back_populates='users')
    address = so.relationship('Address', back_populates='user', uselist=False)  # One-to-one relationship with Address
    families = so.relationship('Family', secondary='family_members', back_populates='members')
    family_members = so.relationship('FamilyMembers', back_populates='user', overlaps='families')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return 'admin' in [role.name for role in self.roles]
    
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
    
    def get_active_family(self):
        if self.active_family_id:
            return Family.query.get(self.active_family_id)
        return None

    def set_active_family(self, family_id):
        family = Family.query.get(family_id)
        if family and family in self.families:
            self.active_family_id = family_id
            return True
        return False
    
    def is_family_owner(self, family):
        return family.owner_id == self.id

    def is_family_co_owner(self, family):
        family_member = FamilyMembers.query.filter_by(user_id=self.id, family_id=family.id).first()
        return family_member and family_member.role_in_family == 'co-owner'

    def is_family_member_of(self, family):
        return family in self.families
    
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
    


## ROLE MANAGEMENT
class Role(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), index=True, unique=True)

    # Relationships
    users = so.relationship('User', secondary='user_roles', back_populates='roles')
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)
    

class UserRoles(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    role_id = db.Column(Integer, db.ForeignKey('role.id'), default=2)

## FAMILY MANAGEMENT
class Family(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), index=True, unique=True, nullable=False)
    owner_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(DateTime, default=func.now())
    invitation_code = db.Column(String(64), unique=True, nullable=False)  # New field

    # Relationships
    owner = so.relationship('User', backref='owned_families', foreign_keys=[owner_id])
    members = so.relationship('User', secondary='family_members', back_populates='families')
    family_members = so.relationship('FamilyMembers', back_populates='family', overlaps='members')
    

    def __repr__(self):
        return f'<Family {self.name}>'
    
    def generate_invitation_code(self):
        """Generate a unique invitation code for this family."""
        self.invitation_code = str(uuid.uuid4())

    def __init__(self, name, owner_id):
        """Ensure an invitation code is always set upon initialization."""
        self.name = name
        self.owner_id = owner_id
        self.generate_invitation_code()




# Association Table for Family Members
class FamilyMembers(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    family_id = db.Column(Integer, db.ForeignKey('family.id'), nullable=False)
    role_in_family = db.Column(String(64), default='member')  # e.g., 'owner', 'co-owner', 'member'

    # Relationships
    family = so.relationship("Family", backref="family_associations", overlaps="members")
    user = so.relationship("User", backref="user_associations", overlaps="families")

    # Define unique constraint to prevent duplicate user-family entries
    __table_args__ = (db.UniqueConstraint('user_id', 'family_id', name='_user_family_uc'),)

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