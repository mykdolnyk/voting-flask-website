from flask_wtf import FlaskForm
from wtforms import RadioField, StringField


class PollVotingForm(FlaskForm):
    choice = RadioField(label='Choose an option:')


class PollVotingFormWithUsername(PollVotingForm):
    username = StringField(label='Enter Your Username:')
