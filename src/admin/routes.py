from flask.blueprints import Blueprint
from config import ADMIN_URL_PREFIX


admin_blueprint = Blueprint('admin', __name__, url_prefix=ADMIN_URL_PREFIX)


@admin_blueprint.route('/auth', methods=['POST'])
def admin_auth():
    return "This is an Admin Auth page."


@admin_blueprint.route('/', methods=['GET', 'POST'])
def admin_dashboard():
    return "This is an Admin Dashboard page."


@admin_blueprint.route('/new-poll', methods=['GET', 'POST'])
def admin_new_poll():
    return 'This is a New Poll page'


@admin_blueprint.route('/edit-poll', methods=['GET', 'POST'])
def admin_edit_poll():
    return 'This is an Edit Poll page'


@admin_blueprint.route('/edit-poll', methods=['GET'])
def admin_poll_stats():
    return 'This is a Stats page'
