from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError 
from app import db
import sqlalchemy as sa 
from app.models import User



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    
    create_or_join = RadioField(
        'Family Option',
        choices=[('create', 'Create a New Family'), ('join', 'Join an Existing Family')],
        validators=[DataRequired()]
    )

    family_name = StringField('Family Name', validators=[], default='')
    invitation_code = StringField('Invitation Code', validators=[], default='')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_family_name(self, family_name):
        if self.create_or_join.data == 'create' and not family_name.data:
            raise ValidationError('Family Name is required when creating a new family.')

    def validate_invitation_code(self, invitation_code):
        if self.create_or_join.data == 'join' and not invitation_code.data:
            raise ValidationError('Invitation Code is required when joining a family.')