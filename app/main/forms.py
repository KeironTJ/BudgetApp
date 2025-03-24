from flask_wtf import FlaskForm 
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    content = TextAreaField(
        'Message',
        validators=[
            DataRequired(message="Message content cannot be empty"),
            Length(max=500, message="Message content cannot exceed 500 characters")
        ]
    )
