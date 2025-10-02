from wtforms import BooleanField, DateField, FieldList, Form, FormField, HiddenField, PasswordField, StringField, TimeField
from wtforms import widgets, validators
from datetime import datetime, date, timedelta
from flask_wtf import FlaskForm

def in_7_days():
    return date.today() + timedelta(days=7)

def now():
    return datetime.now().time()


class ChoiceFormField(Form):
    text = StringField('Choice', 
                       widget=widgets.TextInput(),
                       validators=(validators.Length(max=128),))
    id = HiddenField()


class NewPollForm(FlaskForm):
    title = StringField('Poll Title',
                        validators=(validators.DataRequired(),
                                    validators.Length(max=64),))
    description = StringField('Poll Description',
                              widget=widgets.TextArea(),
                              validators=(validators.Length(max=1024),))
    expires_on_date = DateField('Expires on day', widget=widgets.DateInput(), default=in_7_days)
    expires_on_time = TimeField('Expires at (UTC)', widget=widgets.TimeInput(), default=now)
    choices = FieldList(FormField(ChoiceFormField, label='Choice'),
                        label='Choices', min_entries=4)
    hidden = BooleanField('Hidden', default=False)
    username_required = BooleanField('Username is required', default=False)


class EditPollForm(NewPollForm):
    force_expired = BooleanField('Force Expired', default=False)
    
    
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')