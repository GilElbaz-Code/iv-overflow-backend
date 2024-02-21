import os


class Config:
    # MongoDB Configuration
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB_NAME = 'IVOverflow'

    # Flask Configuration
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'TestSecretKeyForDevelopment')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'TestJwtSecretKeyForDevelopment')
    JWT_ALGORITHM = 'HS512'

    # Other Configurations (if needed)
    KEY_LENGTH = int(os.getenv(key="KEY_LENGTH", default=32))

    @staticmethod
    def init_app(app):
        pass
