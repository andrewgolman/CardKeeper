import functools
import logging


def errors_ignore_and_log(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception("Error")
    return wrapped
