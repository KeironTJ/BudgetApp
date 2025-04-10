from flask_wtf import FlaskForm 
from wtforms import TextAreaField, DateField, SubmitField, SelectField, StringField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length
from app.models import User, Role
from app import db
import sqlalchemy as sa

## MealPlanner
class AddMealForm(FlaskForm):
    meal_date = DateField(
        'Meal Date',
        validators=[DataRequired(message="Please enter a valid date")]
    )
    meal_description = TextAreaField(
        'Meal Description',
        validators=[
            DataRequired(message="Meal description cannot be empty"),
            Length(max=500, message="Meal description cannot exceed 500 characters")
        ]
    )
    meal_source = TextAreaField(
        'Meal Source',
        validators=[
            Length(max=500, message="Meal source cannot exceed 500 characters")
        ]
    )
    add_meal = SubmitField('Add Meal')

# Assign Role Form
class AssignRoleForm(FlaskForm):
    username = SelectField('Username', validators=[DataRequired()], choices=[])
    role = SelectField('Role', validators=[DataRequired()], choices=[])
    assign = SubmitField('Assign Role')
    unassign = SubmitField('Unassign Role')

    def __init__(self, *args, **kwargs):
        super(AssignRoleForm, self).__init__(*args, **kwargs)
        self.username.choices = [
            (user.username, user.username) for user in db.session.scalars(sa.select(User)).all()
        ]
        self.role.choices = [
            (role.name, role.name) for role in db.session.scalars(sa.select(Role)).all()
        ]

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is None:
            raise ValidationError('User does not exist.')

    def validate_role(self, role):
        role_names = [role.name for role in db.session.scalars(sa.select(Role)).all()]
        if role.data not in role_names:
            raise ValidationError('Invalid role.')