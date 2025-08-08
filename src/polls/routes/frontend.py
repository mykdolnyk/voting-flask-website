from flask.blueprints import Blueprint


frontend_blueprint = Blueprint('frontend', __name__)


@frontend_blueprint.route('/', methods=['GET', 'POST'])
def current_poll():
    return 'This is an Index page'


@frontend_blueprint.route('/archive/', methods=['GET'])
def poll_archive():
    return 'This is a Poll Archive page'


@frontend_blueprint.route('/archive/<int:id>', methods=['GET'])
def poll_result(id: int):
    return 'This is a Poll Result page'