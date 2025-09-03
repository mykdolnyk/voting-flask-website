import os


DEBUG = (os.getenv('FLASK_DEBUG', 'False').lower() in ['yes', 'true', '1'])
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

STATIC_FOLDER = 'static/'
STATIC_URL_PATH = '/static/'

TEMPLATE_FOLDER = 'templates/'

ADMIN_URL_PREFIX = os.getenv('FLASK_ADMIN_URL_PREFIX', default='admin')