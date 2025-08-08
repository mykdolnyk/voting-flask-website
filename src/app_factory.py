from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from polls import routes as poll_routes
    from admin import routes as admin_routes
    app.register_blueprint(poll_routes.api_blueprint)
    app.register_blueprint(poll_routes.frontend_blueprint)
    app.register_blueprint(admin_routes.admin_blueprint)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    
    from polls.models import Poll, Choice, Vote

    return app