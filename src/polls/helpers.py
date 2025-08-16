import json
from flask import Request, request, session
from polls.models import Choice, Poll, Vote
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
    try:
        voted = voted_before()
    except (TypeError, KeyError, json.JSONDecodeError):
        voted = None
        malformed = True
        
    if voted or malformed:
        return False

    # Check if the provided poll and choice values are valid 
    poll = Poll.get_active_poll() 
    choice: Choice = Choice.query.filter(
        Choice.poll == poll,
        Choice.id == int(request.form.get('choice'))).scalar()
    if not poll or not choice:
        return False

    return True


def voted_before(request: Request, skip_thumbmark=False) -> bool:
    """A function that checks if the user has voted before. It can skip the
    thumbmark check if needed (in cases when it is not possible to retreive
    the thumbmark).

    Args:
        request (Request): Flask Request object.
        skip_thumbmark (bool, optional): Should the thumbmark check be skipped. Defaults to False.

    Returns:
        bool: Did user vote before.
    """
    if not skip_thumbmark:
        fingerprint = json.loads(request.form['tm'])['thumbmark']
    ip_hash = hashing.hash_value(get_ip_address())
    user_id = str(session.get('user_id'))

    active_poll_choices_id = [choice.id for choice in Poll.get_active_poll().choices]
    
    if not skip_thumbmark:
        same_origin_votes = (Vote.query.filter(
            (Vote.ip_hash == ip_hash) | (Vote.user_id == user_id) | (Vote.fingerprint == fingerprint))
            .filter(Vote.choice_id.in_(active_poll_choices_id)))
    else:
        same_origin_votes = (Vote.query.filter(
            (Vote.ip_hash == ip_hash) | (Vote.user_id == user_id))
            .filter(Vote.choice_id.in_(active_poll_choices_id)))
    
    if same_origin_votes.first() is not None:
        # Voted before
        return True
    
    # Not voted before
    return False


def get_ip_address() -> str:
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']
