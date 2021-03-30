import logging
from django.conf import settings
logger = None


class LoggingMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_request(self, request):
        global logger
        if logger is None:
            logging.basicConfig(
                level=logging.DEBUG,
                filename=settings.LOG_FILE,
                filemode='a')
            logger = logging.getLogger(getattr(settings, 'LOG_NAME', 'django'))
            logger.setLevel(logging.DEBUG)
        request.logger = logger
