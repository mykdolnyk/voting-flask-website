from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Import routes/blueprints
    

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    
    from polls.models import Poll, Choice, Vote

    return app