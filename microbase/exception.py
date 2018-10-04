import sys
from structlog import get_logger


class Errors:
    UnknowError = 'Unknown error'
    NotSpecified = 'Not specified'
    NotMatchSpecs = 'Does not match specs'


class ApplicationError(Exception):
    pass


class RouteError(Exception):
    pass


log = get_logger('service')


def log_uncaught(exc_type, exc_value, exc_tb):
    import traceback
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return

    log.error(str(exc_value), traceback='\n'.join(traceback.format_tb(exc_tb)), exc_info=1)
    sys.exit(1)
