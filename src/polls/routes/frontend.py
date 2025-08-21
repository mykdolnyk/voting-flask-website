from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import request, session
from polls.forms import PollVotingForm
from polls.helpers import voted_before
from polls.models import Poll
from uuid import uuid4

frontend_blueprint = Blueprint('frontend', __name__, 
                               template_folder='../templates/frontend')


@frontend_blueprint.route('/', methods=['GET'])
def current_poll():
    context = {}
    
    poll = Poll.get_active_poll()
    
    if poll:
        form = PollVotingForm()
        form.choice.choices = [(choice.id, choice.text) for choice in poll.choices]

        context['poll'] = poll
        context['form'] = form
        
        context['voted_before'] = voted_before(request, skip_thumbmark=True)
        
    else:
        context['poll'] = None
        context['form'] = None
    
    if not session.get('user_id'):
        session['user_id'] = uuid4()
        session.permanent = True
        
    return render_template('current_poll.html', **context)


@frontend_blueprint.route('/archive/', methods=['GET'])
def poll_archive():
    poll_list = Poll.query.order_by(Poll.id.desc()).all()
    return render_template('poll_archive.html', poll_list=poll_list)


@frontend_blueprint.route('/archive/<int:id>', methods=['GET'])
def poll_results(id: int):
    poll_title = Poll.query.get_or_404(id).title
    return render_template('poll_results.html', poll_title=poll_title)
