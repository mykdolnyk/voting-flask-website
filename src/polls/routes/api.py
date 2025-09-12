import json
from flask.blueprints import Blueprint
from flask import request, session, url_for, jsonify
from polls.forms import PollVotingForm
from polls.models import Choice, Poll, Vote
from polls.helpers import extract_public_poll_info, verify_vote, get_ip_address
from app_factory import db, hashing, redis_client


api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/polls', methods=['GET'])
def get_poll_list():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    
    cached_result = redis_client.get(f"get_poll_list:page-{page};per_page:{per_page}")
    if cached_result:
        return jsonify(json.loads(cached_result))
    
    poll_page = (Poll.query
                 .order_by(Poll.id.desc())
                 .filter(Poll.hidden == False)
                 .paginate(page=page, per_page=per_page, error_out=False))
    
    if len(poll_page.items) <= 0:
        return jsonify([])

    result = [
        {'title': poll.title,
         'id': poll.id,
         'expires_on': poll.expires_on.strftime('%d-%m-%Y, %H:%M'),
         'total_votes': poll.total_votes,
         'current_winner': poll.current_winner.text if poll.current_winner else '',
         'url': url_for('frontend.poll_results', id=poll.id)}
        for poll in poll_page
    ]

    if result:
        redis_client.set(f"get_poll_list:page-{page};per_page:{per_page}", json.dumps(result), ex=60*30)
        return jsonify(result)


@api_blueprint.route('/polls/<int:id>', methods=['GET'])
def get_poll_info(id: int):
    poll: Poll = Poll.query.filter(Poll.hidden == False,
                                   Poll.id == id)

    result = extract_public_poll_info(poll)

    return jsonify(result)


@api_blueprint.route('/vote', methods=['POST'])
def submit_vote():
    poll = Poll.get_active_poll()
    form = poll.get_poll_form()
    form.process(request.form)

    ip_hash = hashing.hash_value(get_ip_address())
    fingerprint = json.loads(request.form.get('tm', '{}')).get('thumbmark')
    user_id = str(session.get('user_id'))

    try:
        username: str = form.username.data
    except AttributeError:
        username = None
    
    choice_id = form.choice.data
    if choice_id is None:
        return jsonify({
            'success': False,
        })
    
    choice: Choice = Choice.query.get(int(choice_id))

    if verify_vote(request):
        new_vote = Vote(ip_hash=ip_hash,
                        fingerprint=fingerprint,
                        user_id=user_id,
                        username=username)
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
                               username=username,
                               failed=True,
                               choice=choice,
                               )
        db.session.add(failed_new_vote)
        db.session.commit()

        return jsonify({
            'success': False,
        })
