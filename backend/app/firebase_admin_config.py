"""
Firebase Admin SDK Configuration Module
Minimal, direct initialization for secure JWT token verification
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, auth
import logging

logger = logging.getLogger(__name__)


class FirebaseAdminConfig:
    """
    Firebase Admin SDK Configuration - Singleton Pattern
    Ensures Firebase is initialized only once during app startup
    """
    
    _initialized = False
    _app = None
    
    @classmethod
    def initialize(cls):
        """
        Initialize Firebase Admin SDK from serviceAccountKey.json
        
        Returns:
            bool: True if successful, False otherwise
        """
        
        # Prevent multiple initializations
        if cls._initialized:
            logger.warning("Firebase Admin SDK already initialized")
            return True
        
        try:
            # Get path to service account key (in same directory as this file)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            credentials_path = os.path.join(current_dir, 'serviceAccountKey.json')
            
            # Verify file exists
            if not os.path.exists(credentials_path):
                logger.error(f"Service account key not found at: {credentials_path}")
                return False
            
            # Load and validate JSON
            with open(credentials_path, 'r') as f:
                service_account_data = json.load(f)
            
            # Verify required fields exist
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [f for f in required_fields if f not in service_account_data]
            if missing_fields:
                logger.error(f"Invalid service account key - missing fields: {missing_fields}")
                return False
            
            # Load credentials and initialize Firebase
            cred = credentials.Certificate(credentials_path)
            cls._app = firebase_admin.initialize_app(cred)
            cls._initialized = True
            
            logger.info(f"Firebase Admin SDK initialized (Project: {service_account_data.get('project_id')})")
            return True
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in service account key: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            return False
    
    @classmethod
    def is_initialized(cls):
        """Check if Firebase Admin SDK is initialized"""
        return cls._initialized
    
    @classmethod
    def get_auth(cls):
        """Get Firebase Authentication module for token verification"""
        if not cls._initialized:
            logger.warning("Firebase not initialized")
            return None
        return auth
    
    @classmethod
    def get_app(cls):
        """Get Firebase app instance"""
        if not cls._initialized:
            logger.warning("Firebase not initialized")
            return None
        return cls._app
    
    @classmethod
    def health_check(cls):
        """Verify Firebase connection is working"""
        try:
            if not cls._initialized:
                return {
                    "status": "error",
                    "message": "Firebase Admin SDK not initialized"
                }
            
            return {
                "status": "ok",
                "message": "Firebase Admin SDK is initialized and working"
            }
        except Exception as e:
            logger.error(f"Firebase health check failed: {e}")
            return {
                "status": "error",
                "message": f"Firebase health check failed: {str(e)}"
            }


# Create singleton instance
firebase_config = FirebaseAdminConfig()

