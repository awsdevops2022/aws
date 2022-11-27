import logging

def log(func):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
        fn_name = func.__name__
        logging.info(f'{fn_name} started...')
        response = func(*args, **kwargs)
        logging.info(f'{fn_name} completed...')
    return wrapper
