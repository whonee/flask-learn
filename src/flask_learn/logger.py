from logging.config import dictConfig
from pathlib import Path

logs_dir = Path('logs')
logs_dir.mkdir(parents=True, exist_ok=True)

dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(name)s in %(module)s: %(message)s',
        },
        'full': {
            'format': '[%(asctime)s] %(levelname)s %(name)s in %(module)s:%(lineno)d: %(message)s ',
        },
        'wsgi': {
            'format': '%(name)s %(message)s',
        },
    },
    'handlers': {
        'root': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': f'{logs_dir}/root.log',
        },
        'error': {
            'class': 'logging.FileHandler',
            'formatter': 'full',
            'filename': f'{logs_dir}/error.log',
        },
        'app': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': f'{logs_dir}/app.log',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['root'],
    },
    'loggers': {
        'error': {
            'level': 'DEBUG',
            'handlers': ['error'],
        },
        'app': {
            'level': 'INFO',
            'handlers': ['app'],
            'propagate': False,
        },
    },
}
