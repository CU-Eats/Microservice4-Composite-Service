import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request received: {request.method} {request.path}")

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(
            f"Response: {response.status_code} {request.method} {request.path} "
            f"Duration: {duration:.2f}s"
        )

        return response
