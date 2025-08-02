import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    TRANSLATION_CHUNK_SIZE = 500  # Characters per chunk
    RATE_LIMIT = "10 per minute"
