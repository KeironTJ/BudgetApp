from flask_wtf import FlaskForm 
from wtforms import TextAreaField, DateField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    content = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Message content cannot be empty"),
            Length(max=500, message="Message content cannot exceed 500 characters")
        ]
    )

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