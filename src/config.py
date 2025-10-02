import os


DEBUG = (os.getenv('FLASK_DEBUG', 'False').lower() in ['yes', 'true', '1'])
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"

STATIC_FOLDER = 'staticfiles/'
STATIC_URL_PATH = '/static/'

TEMPLATE_FOLDER = 'templates/'

ADMIN_URL_PREFIX = os.getenv('FLASK_ADMIN_URL_PREFIX', default='admin')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s in %(funcName)s, %(filename)s: %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s - %(levelname)s in %(funcName)s, %(pathname)s on line %(lineno)d by %(name)s: %(message)s'
        }
    },

    'handlers': {
        'stdout': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'error_log': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': '/var/log/pinlandvote/error.log',
        },
    },

    'loggers': {
        'admin.routes': {
            'handlers': {'stdout', 'error_log'},
            'level': 'ERROR',
            'propagate': False
        }
    },
    
    'root': {
        'handlers': ['stdout', 'error_log'],
        'level': 'ERROR'
    }
}
