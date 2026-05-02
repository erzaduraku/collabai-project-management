import logging
import time

from common.utils import client_ip

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000
        logger.info(
            '%s %s -> %s (%.2f ms) ip=%s',
            request.method,
            request.path,
            getattr(response, 'status_code', '?'),
            duration_ms,
            client_ip(request) or '-',
        )
        return response
