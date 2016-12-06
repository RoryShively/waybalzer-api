from datetime import timedelta

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

SERVER_NAME = '0.0.0.0'
SECRET_KEY = 'secret'

# CELERY.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5

# SQLAlchemy.
db_uri = 'postgresql://wayblazer:devpassword@postgres:5432/wayblazer'
# db_uri = 'postgres:///wayblazer'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Emit signals when object changes

# User.
SEED_ADMIN_EMAIL = 'roryshively1@gmail.com'
SEED_ADMIN_PASSWORD = 'asdfasdf'
REMEMBER_COOKIE_DURATION = timedelta(days=90)
