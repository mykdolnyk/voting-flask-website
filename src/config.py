import os


DEBUG = (os.getenv('FLASK_DEBUG', 'False').lower() in ['yes', 'true', '1'])
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

STATIC_FOLDER = 'static/'
STATIC_URL_PATH = '/static/'

TEMPLATE_FOLDER = 'templates/'

ADMIN_URL_PREFIX = os.getenv('FLASK_ADMIN_URL_PREFIX', default='/admin')