from flask_wtf import FlaskForm 
from wtforms import TextAreaField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

## Meal Planner
class AddMealForm(FlaskForm):
    meal_date = DateField(
        'Meal Date',
        validators=[DataRequired(message="Please enter a valid date")]
    )
    meal_title = StringField(
        'Meal Title',
        validators=[
            DataRequired(message="Meal title cannot be empty"),
            Length(max=64, message="Meal title cannot exceed 64 characters")
        ]
    )

    meal_description = TextAreaField(
        'Meal Description',
        validators=[Length(max=500, message="Meal description cannot exceed 500 characters")]
    )
    meal_source = TextAreaField(
        'Meal Source',
        validators=[
            Length(max=500, message="Meal source cannot exceed 500 characters")
        ]
    )
    add_meal = SubmitField('Add Meal')