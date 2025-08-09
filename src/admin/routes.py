from flask.blueprints import Blueprint
from config import ADMIN_URL_PREFIX
from flask.templating import render_template
from flask import request
from admin.forms import NewPollForm
from polls.models import Poll, Choice
from app_factory import db
import datetime

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix=ADMIN_URL_PREFIX,
                            template_folder='templates/admin')


@admin_blueprint.route('/auth', methods=['POST'])
def auth():
    return "This is an Admin Auth page."


@admin_blueprint.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@admin_blueprint.route('/new-poll', methods=['GET', 'POST'])
def new_poll():
    context = {}
    
    form = NewPollForm(request.form)
    
    if request.method == 'GET':
        context['form'] = form

    else:
        if form.validate_on_submit():
            print(form.data)
            
            expires_on = datetime.datetime.combine(form.expires_on_date.data,
                                                   form.expires_on_time.data)
            
            try:
                poll = Poll(title=form.title.data,
                            description=form.description.data,
                            expires_on=expires_on,
                            hidden=form.hidden.data,
                            )
                db.session.add(poll)
                
                for choice_field in form.choices:
                    choice = Choice(text=choice_field.text.data,
                                    poll=poll)
                    db.session.add(choice)
                
                db.session.commit()

            except Exception:
                # Todo: Log that somewhere
                form.form_errors.append('Something went wrong.')
     
    context['form'] = form   
    return render_template('new_poll.html', **context)


@admin_blueprint.route('/edit-poll/<int:id>', methods=['GET', 'POST'])
def edit_poll(id: int):
    return render_template('edit_poll.html')


@admin_blueprint.route('/stats/<int:id>', methods=['GET'])
def poll_stats(id: int):
    return render_template('poll_stats.html')

