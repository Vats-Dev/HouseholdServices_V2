from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()

# Configuration settings
class Config:
    
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/4"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/5"
    REDIS_URL = "redis://localhost:6379/6"
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 7
    SECRET_KEY = getenv('SECRET_KEY')
    JWT_SECRET_KEY = getenv('SECRET_KEY')

    SMTP_SERVER_HOST = 'localhost'
    SMTP_SERVER_PORT = 1025
    SMTP_SERVER_EMAIL = 'noreply@localhost'
    SMTP_SERVER_PASSWORD = 'password'
