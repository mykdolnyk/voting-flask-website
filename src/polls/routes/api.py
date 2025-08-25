import json
import flask
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
    poll_page = (Poll.query
                 .order_by(Poll.id.desc())
                 .filter(Poll.hidden == False)
                 .paginate(page=page, per_page=4, error_out=False))
    
    if len(poll_page.items) <= 0:
        return jsonify([])

    result = [
        {'title': poll.title,
         'id': poll.id,
         'expires_on': poll.expires_on,
         'total_votes': poll.total_votes,
         'current_winner': poll.current_winner.text,
         'url': url_for('frontend.poll_results', id=poll.id)}
        for poll in poll_page
    ]

    if result:
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

    ip_hash = hashing.hash_value(get_ip_address())
    fingerprint = json.loads(request.form.get('tm', '{}')).get('thumbmark')
    user_id = str(session.get('user_id'))

    poll = Poll.get_active_poll()
    choice: Choice = Choice.query.get(int(form.choice.data))

    if verify_vote(request):
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
        failed_new_vote = Vote(ip_hash=ip_hash,
                               fingerprint=fingerprint,
                               user_id=user_id,
                               failed=True,
                               choice=choice,
                               )
        db.session.add(failed_new_vote)
        db.session.commit()

        return jsonify({
            'success': False,
        })
