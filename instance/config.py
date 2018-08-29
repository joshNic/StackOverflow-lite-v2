
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEVELOPMENT = True
    # DATABASE_URI = ''

class TestingConfig(BaseConfig):
    TESTING = True
    # DATABASE_URI = ''
