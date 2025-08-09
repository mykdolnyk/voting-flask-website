from flask.blueprints import Blueprint
from flask.templating import render_template


frontend_blueprint = Blueprint('frontend', __name__, 
                               template_folder='../templates/frontend')


@frontend_blueprint.route('/', methods=['GET', 'POST'])
def current_poll():
    return render_template('current_poll.html')


@frontend_blueprint.route('/archive/', methods=['GET'])
def poll_archive():
    return render_template('poll_archive.html')


@frontend_blueprint.route('/archive/<int:id>', methods=['GET'])
def poll_results(id: int):
    return render_template('poll_results.html')
