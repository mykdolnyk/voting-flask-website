from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_hashing import Hashing
from flask_redis import FlaskRedis


db = SQLAlchemy()
migrate = Migrate()
hashing = Hashing()
login_manager = LoginManager()
redis_client = FlaskRedis()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from polls import routes as poll_routes
    from admin import routes as admin_routes
    import admin.commands  
    app.register_blueprint(poll_routes.api_blueprint)
    app.register_blueprint(poll_routes.frontend_blueprint)
    app.register_blueprint(admin_routes.admin_blueprint)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    hashing.init_app(app=app)
    login_manager.init_app(app=app)
    redis_client.init_app(app=app)
    
    from polls.models import Poll, Choice, Vote, User
    @login_manager.user_loader
    def user_loader(user_id: str):
        return User.query.get(int(user_id))


    return app