import os


DEBUG = (os.getenv('FLASK_DEBUG', 'False').lower() in ['yes', 'true', '1'])
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"