class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///studio_nagran.db'
    SQLALCHEMY_ECHO = True
