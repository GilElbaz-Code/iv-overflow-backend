import os


class Config:
    # MongoDB Configuration
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB_NAME = 'IVOverflow'

    # Flask Configuration
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'n-Fj0UziJrXl_lnYIQsmd8riaC8W6ToNxM1iNU-UkTA')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'N9bHtf2Y1IUmqkzGO0IGNNwFvpP2hi5eoLTbbSpx8Dc')
