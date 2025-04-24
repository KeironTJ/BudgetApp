from flask_wtf import FlaskForm 
from wtforms import TextAreaField, SelectField, SubmitField, RadioField, StringField
from wtforms.validators import DataRequired, Length, ValidationError 
from app.models import User, Family, FamilyMembers

class FamilySelectForm(FlaskForm):
    family = SelectField('Select Family', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Choose Family')

class FamilyCreateorJoinForm(FlaskForm): 
    create_or_join = RadioField(
        'Family Option',
        choices=[('create', 'Create a New Family'), ('join', 'Join an Existing Family')],
        validators=[DataRequired()]
    )

    family_name = StringField('Family Name', validators=[], default='')
    invitation_code = StringField('Invitation Code', validators=[], default='')
    submit = SubmitField('Register')

        
    def validate_family_name(self, family_name):
        if self.create_or_join.data == 'create' and not family_name.data:
            raise ValidationError('Family Name is required when creating a new family.')

    def validate_invitation_code(self, invitation_code):
        if self.create_or_join.data == 'join' and not invitation_code.data:
            raise ValidationError('Invitation Code is required when joining a family.')