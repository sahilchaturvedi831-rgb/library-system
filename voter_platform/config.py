import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'voter-platform-secret-key-2024')
    
    # Database
    DB_FILE = os.environ.get('DB_FILE', 'voter_platform.db')
    
    # AI Configuration
    PROFILING_ENABLED = True
    SENTIMENT_ANALYSIS_ENABLED = True
    PREDICTIONS_ENABLED = True
    
    # Pagination
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 500
    
    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE = 60
