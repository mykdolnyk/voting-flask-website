from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import request
from polls.forms import PollVotingForm
from polls.models import Poll


frontend_blueprint = Blueprint('frontend', __name__, 
                               template_folder='../templates/frontend')


@frontend_blueprint.route('/', methods=['GET'])
def current_poll():
    context = {}
    
    poll = Poll.get_active_poll()
    form = PollVotingForm()
    
    form.choice.choices = [(choice.id, choice.text) for choice in poll.choices]

    context['poll'] = poll
    context['form'] = form
    
    return render_template('current_poll.html', **context)


@frontend_blueprint.route('/archive/', methods=['GET'])
def poll_archive():
    return render_template('poll_archive.html')


@frontend_blueprint.route('/archive/<int:id>', methods=['GET'])
def poll_results(id: int):
    poll_title = Poll.query.get_or_404(id).title
    return render_template('poll_results.html', poll_title=poll_title)
