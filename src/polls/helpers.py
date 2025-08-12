import json
from flask import Request, request, session
from polls.models import Poll, Vote
from app_factory import hashing


def extract_public_poll_info(poll: Poll):
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

    return result


def verify_vote(request: Request) -> bool:
    fingerprint_data = json.loads(request.form.get('tm'))

    try:
        fingerprint = fingerprint_data['thumbmark']
        ip_hash = hashing.hash_value(get_ip_address())
        user_id = str(session['user_id'])
    except (TypeError, KeyError):
        return False

    active_poll_choices_id = [choice.id for choice in Poll.get_active_poll().choices]
    
    same_origin_votes = (Vote.query.filter(
        (Vote.ip_hash == ip_hash) | (Vote.user_id == user_id) | (Vote.fingerprint == fingerprint))
        .filter(Vote.choice_id.in_(active_poll_choices_id)))

    if same_origin_votes.first() is not None:
        return False

    return True


def get_ip_address() -> str:
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
