import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API errors with status code and message."""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
        
    def to_dict(self):
        """Convert error to dictionary for JSON response."""
        error_dict = dict(self.payload or {})
        error_dict['error'] = self.message
        return error_dict

def register_error_handlers(app):
    """
    Register error handlers for the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
        
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle HTTP exceptions."""
        response = jsonify({
            'error': error.description,
            'code': error.code
        })
        response.status_code = error.code
        return response
        
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle all other exceptions."""
        logger.exception("Unhandled exception occurred")
        response = jsonify({
            'error': 'An unexpected error occurred',
            'details': str(error)
        })
        response.status_code = 500
        return response

# Common error classes
class ValidationError(APIError):
    """Error for invalid input data."""
    def __init__(self, message, payload=None):
        super().__init__(message, 400, payload)

class NotFoundError(APIError):
    """Error for resource not found."""
    def __init__(self, message, payload=None):
        super().__init__(message, 404, payload)

class DatabaseError(APIError):
    """Error for database operations."""
    def __init__(self, message, payload=None):
        super().__init__(message, 500, payload)

class AIProcessingError(APIError):
    """Error for AI processing failures."""
    def __init__(self, message, payload=None):
        super().__init__(message, 500, payload)