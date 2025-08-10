from flask_wtf import FlaskForm
from wtforms import RadioField


class PollVotingForm(FlaskForm):
    choice = RadioField(label='Choose an option:')
