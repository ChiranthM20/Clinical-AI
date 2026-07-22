"""
Firebase Authentication Middleware
Provides decorator for verifying Firebase ID tokens and extracting user info
"""

from functools import wraps
from flask import request, jsonify, g
from firebase_admin import exceptions
import logging

logger = logging.getLogger(__name__)


def verify_firebase_token(f):
    """
    Decorator to verify Firebase ID token from Authorization header
    
    Expected header format: Authorization: Bearer <firebase_id_token>
    
    On success:
    - Stores user info in g.user_id (accessible in route handler)
    - Stores full decoded token in g.firebase_token (optional)
    
    On failure:
    - Returns JSON error response with 401 status
    - Does NOT call the decorated function
    
    Usage in route:
        @app.route("/protected", methods=["POST"])
        @verify_firebase_token
        def protected_route():
            user_id = g.user_id  # Access authenticated user
            return jsonify({"message": f"Hello {user_id}"})
    
    Error responses:
    - 401: Missing token, invalid format, expired, invalid signature, etc.
    """
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        # Validate header format: "Bearer <token>"
        if not auth_header:
            logger.warning("Missing Authorization header")
            return jsonify({
                "error": "Unauthorized",
                "message": "Missing Authorization header"
            }), 401
        
        if not auth_header.startswith('Bearer '):
            logger.warning("Invalid Authorization header format")
            return jsonify({
                "error": "Unauthorized",
                "message": "Authorization header must start with 'Bearer '"
            }), 401
        
        # Extract token
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        if not token:
            logger.warning("Empty token in Authorization header")
            return jsonify({
                "error": "Unauthorized",
                "message": "Token cannot be empty"
            }), 401
        
        try:
            # Import Firebase auth here to avoid circular imports
            from firebase_admin_config import firebase_config
            
            # Check if Firebase is initialized
            if not firebase_config.is_initialized():
                logger.error("Firebase Admin SDK not initialized")
                return jsonify({
                    "error": "Internal Server Error",
                    "message": "Authentication service not available"
                }), 503
            
            # Get Firebase auth module
            auth_module = firebase_config.get_auth()
            if not auth_module:
                logger.error("Firebase auth module not available")
                return jsonify({
                    "error": "Internal Server Error",
                    "message": "Authentication service not available"
                }), 503
            
            # Verify token using Firebase Admin SDK
            # This validates:
            # - Token signature
            # - Token expiration
            # - Token issued by Firebase
            # - Token is for correct Firebase project
            try:
                decoded_token = auth_module.verify_id_token(token)
            except Exception as token_error:
                logger.warning(f"Token verification failed: {type(token_error).__name__}: {str(token_error)}")
                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid or malformed token"
                }), 401
            
            # Extract user_id from token claims
            user_id = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            if not user_id:
                logger.warning("Token missing uid claim")
                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid token claims"
                }), 401
            
            # Store user info in Flask g object (request-scoped)
            g.user_id = user_id
            g.email = email
            g.firebase_token = decoded_token
            
            logger.debug(f"Token verified for user: {user_id}")
            
            # Call the protected route handler
            return f(*args, **kwargs)
        
        except exceptions.ExpiredSignatureError:
            logger.warning("Token expired")
            return jsonify({
                "error": "Unauthorized",
                "message": "Token has expired"
            }), 401
        
        except exceptions.InvalidSignatureError:
            logger.warning("Invalid token signature")
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid token signature"
            }), 401
        
        except exceptions.InvalidIdTokenError as e:
            logger.warning(f"Invalid ID token: {str(e)}")
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid or malformed token"
            }), 401
        
        except ValueError as e:
            logger.warning(f"Value error in token verification: {str(e)}")
            return jsonify({
                "error": "Unauthorized",
                "message": "Invalid or malformed token"
            }), 401
        
        except Exception as e:
            logger.error(f"Token verification error: {type(e).__name__}: {str(e)}")
            return jsonify({
                "error": "Unauthorized",
                "message": "Token verification failed"
            }), 401
    
    return decorated_function


def get_user_id():
    """
    Helper function to get authenticated user_id from Flask g object
    
    Usage in route handler:
        @app.route("/protected")
        @verify_firebase_token
        def protected():
            user_id = get_user_id()
            # Your logic here
    
    Returns:
        str: user_id if authenticated, None otherwise
    """
    return getattr(g, 'user_id', None)


def get_user_email():
    """
    Helper function to get authenticated user email from Flask g object
    
    Returns:
        str: email if available, None otherwise
    """
    return getattr(g, 'email', None)


def get_firebase_token():
    """
    Helper function to get full decoded Firebase token from Flask g object
    
    Returns:
        dict: Full decoded token if available, None otherwise
    """
    return getattr(g, 'firebase_token', None)
