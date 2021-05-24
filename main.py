import logging.config
from fitness_web_app import app

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '%(name)s %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file_logger': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'tracker.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
        'console_logger': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'basic',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        '__main__': {
            'handlers': ['file_logger', 'console_logger'],
            'level': 'WARNING',
            'propagate': False
        }
    },
    'root': {
        'handlers': ['file_logger'],
        'level': 'ERROR',
    }
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


def main():
    app.run()


if __name__ == '__main__':
    main()
