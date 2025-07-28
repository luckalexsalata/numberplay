import logging
import time
import json
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get token from query parameters
        query_string = scope.get('query_string', b'').decode()
        query_params = dict(x.split('=') for x in query_string.split('&') if x)
        token = query_params.get('token', None)
        
        if token:
            try:
                # Lazy imports to avoid Django app registry issues
                from rest_framework_simplejwt.tokens import AccessToken
                from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
                from django.contrib.auth.models import AnonymousUser
                
                # Validate JWT token
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                
                # Get user from database
                user = await self.get_user(user_id)
                if user:
                    scope['user'] = user
                else:
                    scope['user'] = AnonymousUser()
            except (InvalidToken, TokenError, KeyError):
                from django.contrib.auth.models import AnonymousUser
                scope['user'] = AnonymousUser()
        else:
            from django.contrib.auth.models import AnonymousUser
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
    
    @database_sync_to_async
    def get_user(self, user_id):
        try:
            from auth_app.models import User
            return User.objects.get(id=user_id)
        except:
            return None 

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging API requests and responses"""
    
    def process_request(self, request):
        """Log incoming request"""
        request.start_time = time.time()
        
        # Log request details
        log_data = {
            'method': request.method,
            'path': request.path,
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'ip': self.get_client_ip(request),
        }
        
        logger.info(f"Request: {json.dumps(log_data)}")
    
    def process_response(self, request, response):
        """Log response details"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration': f"{duration:.3f}s",
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
            }
            
            logger.info(f"Response: {json.dumps(log_data)}")
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ExceptionLoggingMiddleware(MiddlewareMixin):
    """Middleware for logging exceptions"""
    
    def process_exception(self, request, exception):
        """Log exceptions with detailed information"""
        log_data = {
            'method': request.method,
            'path': request.path,
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'ip': self.get_client_ip(request),
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
        }
        
        logger.error(f"Exception: {json.dumps(log_data)}", exc_info=True)
        
        # Return JSON error response for API requests
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Internal server error',
                'detail': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 