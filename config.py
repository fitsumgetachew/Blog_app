import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY ='dev'
TESTING = True
DEBUG = True
PROPAGATE_EXCEPTIONS = True
TRAP_hTTP_EXCEPTIONS = True
TRAP_BAD_REQEUST_ERRORS = True

PERMANENT_SESSION_LIFETIME = 5
REMEMBER_COOKIE_DURAION = 60