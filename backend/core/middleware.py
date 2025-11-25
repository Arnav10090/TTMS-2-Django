import logging
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests
    """
    def process_request(self, request):
        logger.info(f"{request.method} {request.path}")
        return None
    
    def process_response(self, request, response):
        logger.info(f"{request.method} {request.path} - {response.status_code}")
        return response


class AppAvailabilityMiddleware(MiddlewareMixin):
    """
    Middleware to check if requested app is available
    """
    def process_request(self, request):
        from core.utils import is_app_enabled
        
        path = request.path
        
        if path.startswith('/api/ttms/') and not is_app_enabled('ttms'):
            return Response({'error': 'TTMS app is not enabled'}, status=404)
        
        if path.startswith('/api/ptms/') and not is_app_enabled('ptms'):
            return Response({'error': 'PTMS app is not enabled'}, status=404)
        
        return None
