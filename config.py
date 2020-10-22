import os



class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
    AWS_S3_DOMAIN               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    BRAIN_MERCHANT_ID                 = os.environ.get("BT_MERCHANT_ID")
    BRAIN_PUBLIC_KEY                 = os.environ.get("BT_PUBLIC_KEY")
    BRAIN_PRIVATE_KEY                 = os.environ.get("BT_PRIVATE_KEY")


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
