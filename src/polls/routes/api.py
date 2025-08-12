import json
from flask.blueprints import Blueprint
from flask import request, session, url_for, jsonify
from polls.forms import PollVotingForm
from polls.models import Choice, Poll, Vote
from polls.helpers import extract_public_poll_info, verify_vote, get_ip_address
from app_factory import db, hashing


api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/polls', methods=['GET'])
def get_poll_list():
    page = request.args.get('page', 1, type=int)
    poll_page = Poll.query.filter(
        Poll.hidden == False).paginate(page=page, per_page=5)

    result = [
        {'title': poll.title,
         'id': poll.id,
         'url': url_for('frontend.poll_results', id=poll.id)}
        for poll in poll_page
    ]

    return jsonify(result)


@api_blueprint.route('/polls/<int:id>', methods=['GET'])
def get_poll_info(id: int):
    poll: Poll = Poll.query.filter(Poll.hidden == False,
                                   Poll.id == id)

    result = extract_public_poll_info(poll)

    return jsonify(result)


@api_blueprint.route('/vote', methods=['POST'])
def submit_vote():
    form = PollVotingForm(request.form)
 
    if verify_vote(request):
        poll = Poll.get_active_poll() 
        choice: Choice = Choice.query.filter(
            Choice.poll == poll,
            Choice.id == int(form.choice.data)).scalar()
        
        if not poll or not choice:
            return jsonify({
                'success': False,
            })

        ip_hash = hashing.hash_value(get_ip_address())
        fingerprint = json.loads(request.form['tm']).get('thumbmark')
        user_id = str(session['user_id'])
        
        new_vote = Vote(ip_hash=ip_hash,
                        fingerprint=fingerprint,
                        user_id=user_id)
        choice.votes.append(new_vote)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'poll_data': extract_public_poll_info(poll),
        })
        
    else:
        return jsonify({
            'success': False,
        })
