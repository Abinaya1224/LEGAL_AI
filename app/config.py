class config:
    SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Solidpro%402024@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking
    SECRET_KEY = 'your_secret_key' # Secret key for session management (use a secure key)

    