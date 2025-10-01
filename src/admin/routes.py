import datetime
from flask import flash, jsonify, redirect, request, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import login_user, logout_user
from admin.helpers import clear_cache_keys, superuser_only
from config import ADMIN_URL_PREFIX
from admin.forms import LoginForm, NewPollForm, EditPollForm
from polls.models import Poll, Choice, User, Vote
from app_factory import db
from werkzeug.security import check_password_hash

admin_blueprint = Blueprint('admin', __name__,
                            url_prefix=f"/{ADMIN_URL_PREFIX}",
                            template_folder='templates/admin')


@admin_blueprint.route('/auth', methods=['GET', 'POST'])
def auth():
    context = {}
    if request.method == 'GET':
        form = LoginForm()
        context['form'] = form
        return render_template('auth_page.html', **context)
    
    elif request.method == 'POST':
        form = LoginForm(request.form)
        context['form'] = form
        
        user: User = User.query.filter(User.username == form.username.data).first()
        
        if form.validate_on_submit():
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                flash('Successful login.', category='info')
                return redirect(url_for('admin.dashboard'))
            else:
                form.form_errors.append('Incorrect credentials.')

        return render_template('auth_page.html', **context)


@admin_blueprint.route('/de-auth/', methods=['GET'])
@superuser_only
def de_auth():
    logout_user()
    return redirect(url_for('frontend.current_poll'))


@admin_blueprint.route('/', methods=['GET'])
@superuser_only
def dashboard():
    context = {}

    context['active_poll'] = Poll.get_active_poll()
    context['all_polls'] = Poll.query.order_by(Poll.id.desc()).all()
    context['poll_count'] = len(context['all_polls'])
    context['vote_count'] = Vote.query.filter(Vote.failed == False).count()

    return render_template('dashboard.html', **context)


@admin_blueprint.route('/new-poll', methods=['GET', 'POST'])
@superuser_only
def new_poll():
    context = {}

    form = NewPollForm(request.form)

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        if form.validate_on_submit():
            expires_on = datetime.datetime.combine(form.expires_on_date.data,
                                                   form.expires_on_time.data)
            try:
                poll = Poll(title=form.title.data,
                            description=form.description.data,
                            expires_on=expires_on,
                            hidden=form.hidden.data,
                            username_required=form.username_required.data)

                for choice_data in form.choices.data:
                    if choice_data['text']:
                        choice = Choice(text=choice_data['text'])
                        poll.choices.append(choice)

                db.session.add(poll)
                db.session.commit()
                
                clear_cache_keys("get_poll_list:*")
                clear_cache_keys("voted_before*")
                
                flash(render_template('flashes/success.html',
                                      message='The poll has been successully created.'),
                      'info')
                
                return redirect(url_for('admin.dashboard'))

            except Exception:
                # Todo: Log that somewhere
                form.form_errors.append('Something went wrong.')
                raise

    context['form'] = form
    return render_template('new_poll.html', **context)


@admin_blueprint.route('/edit-poll/<int:id>', methods=['GET', 'POST'])
@superuser_only
def edit_poll(id: int):
    context = {}

    poll: Poll = Poll.query.get_or_404(id)
    choices: Choice = Choice.query.filter(Choice.poll_id == id)

    if request.method == 'GET':
        form = EditPollForm(title=poll.title,
                            description=poll.description,
                            expires_on_date=poll.expires_on.date(),
                            expires_on_time=poll.expires_on.time(),
                            hidden=poll.hidden,
                            force_expired=poll.force_expired,
                            choices=choices,
                            username_required=poll.username_required)

    elif request.method == 'POST':
        form = EditPollForm(request.form)

        if form.validate_on_submit():
            expires_on = datetime.datetime.combine(form.expires_on_date.data,
                                                   form.expires_on_time.data)
            try:
                poll.title = form.title.data
                poll.description = form.description.data
                poll.expires_on = expires_on
                poll.hidden = form.hidden.data
                poll.force_expired = form.force_expired.data
                poll.username_required = form.username_required.data

                for choice_data in form.choices.data:
                    # If it existed before
                    if choice_data['id']:
                        choice: Choice = Choice.query.filter(
                            Choice.poll == poll, Choice.id == int(choice_data['id'])).first()

                    # If it has not existed but a value has been entered
                    elif choice_data['text']:
                        choice = Choice(text=choice_data['text'])
                        poll.choices.append(choice)
                        continue

                    # If it has existed before and the text is not empty
                    if choice_data['text']:
                        choice.text = choice_data['text']

                    # If it has existed before and the text is empty
                    elif choice_data['id']:
                        db.session.delete(choice)

                db.session.commit()
                
                clear_cache_keys("get_poll_list:*")
                clear_cache_keys("voted_before*")
                
                flash(render_template('flashes/success.html',
                                      message='The poll has been successully updated.'),
                      'info')

                return redirect(url_for('admin.dashboard'))

            except Exception:
                # Todo: Log that somewhere
                form.form_errors.append('Something went wrong.')
                raise

    context['form'] = form
    context['poll_id'] = id

    return render_template('edit_poll.html', **context)


@admin_blueprint.route('/stats/<int:id>', methods=['GET'])
@superuser_only
def poll_stats(id: int):
    context = {}
    
    poll: Poll = Poll.query.get_or_404(id)
    context['poll'] = poll
    try:
        context['failed_votes_rate'] = poll.failed_votes_count / (poll.failed_votes_count + poll.total_votes) * 100
    except ZeroDivisionError:
        context['failed_votes_rate'] = 0
        
    raw_votes_over_time = poll.votes_over_time('1h')
    
    if raw_votes_over_time is not None:
        votes_over_time_header = [['Time'] + raw_votes_over_time.columns.to_list()]
        votes_over_time_rows = [[str(time)] + row.to_list() for time, row in raw_votes_over_time.iterrows()]
        votes_over_time = votes_over_time_header + votes_over_time_rows
        
        context['votes_over_time'] = votes_over_time
    else:
        context['votes_over_time'] = []

    return render_template('poll_stats.html', **context)


@admin_blueprint.route('/api/user-choices/<string:username>', methods=['GET'])
@superuser_only
def api_user_choices(username: str):
    poll_id = request.args.get('poll-id', None, type=int)
    votes = Vote.query.filter(Vote.username == username)
    
    if poll_id is not None:
        poll_choices = Choice.query.filter(Choice.poll_id == poll_id).all()
        poll_choice_ids = [choice.id for choice in poll_choices]
        votes = votes.filter(Vote.choice_id.in_(poll_choice_ids))
        
    response = {
        'username': username,
        'choices': {
            vote.choice.poll_id: vote.choice.text for vote in votes.all()
        }
    }

    return jsonify(response)


@admin_blueprint.route('/api/poll-voters/<int:poll_id>', methods=['GET'])
@superuser_only
def api_poll_voters(poll_id: int):
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    poll: Poll = Poll.query.filter(Poll.id == poll_id).first()
    choice_ids = (choice.id for choice in poll.choices)
    
    vote_page = (Vote.query.filter(Vote.choice_id.in_(choice_ids))
                 .paginate(page=page, per_page=per_page, error_out=False))
    
    if len(vote_page.items) > 0:
        result = {vote.username: vote.choice.id for vote in vote_page}
    else: 
        result = {}
    
    response = {
        'poll_id': poll_id,
        'voters': result
    }
    
    return jsonify(response)