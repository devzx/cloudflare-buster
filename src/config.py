import os

DEBUG = False
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY', None)
