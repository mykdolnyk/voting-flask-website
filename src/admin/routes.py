from flask.blueprints import Blueprint
from config import ADMIN_URL_PREFIX
from flask.templating import render_template


admin_blueprint = Blueprint('admin', __name__,
                            url_prefix=ADMIN_URL_PREFIX,
                            template_folder='templates/admin')


@admin_blueprint.route('/auth', methods=['POST'])
def auth():
    return "This is an Admin Auth page."


@admin_blueprint.route('/', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@admin_blueprint.route('/new-poll', methods=['GET', 'POST'])
def new_poll():
    return render_template('new_poll.html')


@admin_blueprint.route('/edit-poll/<int:id>', methods=['GET', 'POST'])
def edit_poll(id: int):
    return render_template('edit_poll.html')


@admin_blueprint.route('/stats/<int:id>', methods=['GET'])
def poll_stats(id: int):
    return render_template('poll_stats.html')

