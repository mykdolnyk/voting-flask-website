from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import request, session
from polls.forms import PollVotingForm
from polls.helpers import get_ip_address, voted_before
from polls.models import Poll
from uuid import uuid4
from app_factory import redis_client, hashing

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
        
        cached_voted = redis_client.get(f'voted_before_skipthumb:{hashing.hash_value(get_ip_address())}')
        if cached_voted is not None:
            voted = int(cached_voted)
        else:
            voted = voted_before(request, skip_thumbmark=True)
            redis_client.set(f'voted_before_skipthumb:{hashing.hash_value(get_ip_address())}', int(True), ex=60*15)
        
        context['voted_before'] = voted
        
    else:
        context['poll'] = None
        context['form'] = None
    
    if not session.get('user_id'):
        session['user_id'] = uuid4()
        session.permanent = True
        
    return render_template('current_poll.html', **context)


@frontend_blueprint.route('/archive/', methods=['GET'])
def poll_archive():
    return render_template('poll_archive.html')


@frontend_blueprint.route('/archive/<int:id>', methods=['GET'])
def poll_results(id: int):
    poll = Poll.query.get_or_404(id)
    return render_template('poll_results.html', poll=poll)
