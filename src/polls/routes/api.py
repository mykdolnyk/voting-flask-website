from flask.blueprints import Blueprint
from flask import request, url_for, jsonify
from polls.models import Poll
from polls.helpers import verify_vote


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

    result = {
        'title': poll.title,
        'id': poll.id,
        'description': poll.description,
        'started_on': poll.started_on,
        'expires_on': poll.expires_on,
        'total_votes': poll.total_votes
    }

    choices = [
        {
            'text': choice.text,
            'total_votes': choice.total_votes
        } for choice in (poll.choices)
    ]

    result['choices'] = choices

    return jsonify(result)


@api_blueprint.route('/vote', methods=['POST'])
def submit_vote():

    if verify_vote(request):
        return jsonify({
            'success': True,
        })
    else:
        return jsonify({
            'success': False,
        })
