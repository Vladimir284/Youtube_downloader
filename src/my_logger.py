import logging
import src.constants as constants

# Create and format logger
logger = logging.getLogger(__name__)
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
logger.addHandler(logger_handler)

if constants.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


# Decorator function for debug log
def debug_log(func):
    """
    Decorator for debug_log, works if Constants.DEBUG=True
    Parameters
    ----------
    func :
        Object of function that is decorated
    Returns
    -------
    Any

    """

    def wrapper(*args, **kwargs):
        """

        Parameters
        ----------
        args : list
        All arguments passed into function
        kwargs : str
        Unpacked list of arguments

        Returns
        -------

        """
        if constants.DEBUG:
            logger.debug("Begin {}".format(func.__name__))
        result = func(*args, **kwargs)
        if constants.DEBUG:
            logger.debug("{} OK".format(func.__name__))
        return result

    return wrapper
