from flask_wtf import FlaskForm 
from wtforms import TextAreaField, DateField, SubmitField, StringField, BooleanField, TimeField
from wtforms.validators import DataRequired, Length

## Messaging
class MessageForm(FlaskForm):
    content = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Message content cannot be empty"),
            Length(max=500, message="Message content cannot exceed 500 characters")
        ]
    )

## Meal Planner
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

## Activity Planner
class AddActivityForm(FlaskForm):
    activity_start_date = DateField(
        'Activity Start Date',
        validators=[DataRequired(message="Please enter a valid date")]
    )
    activity_end_date = DateField(
        'Activity End Date',
        validators=[DataRequired(message="Please enter a valid date")]
    )
    from wtforms.validators import Optional

    activity_start_time = TimeField('Activity Start Time', validators=[Optional()])
    activity_end_time = TimeField('Activity End Time', validators=[Optional()])
    activity_all_day_event = BooleanField('All Day Event')
    activity_title = StringField(
        'Activity Title',
        validators=[
            DataRequired(message="Activity title cannot be empty"),
            Length(max=100, message="Activity title cannot exceed 100 characters")
        ]
    )
    activity_description = TextAreaField(
        'Activity Description',
        validators=[Length(max=500, message="Activity description cannot exceed 500 characters")]
    )
    activity_location = StringField(
        'Activity Location',
        validators=[Length(max=200, message="Activity location cannot exceed 200 characters")]
    )
    activity_comments = TextAreaField(
        'Activity Comments',
        validators=[Length(max=500, message="Activity comments cannot exceed 500 characters")]
    )
    add_activity = SubmitField('Add Activity')