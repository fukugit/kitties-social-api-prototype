class LocalConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://postgres.your-tenant-id:your-super-secret-and-long-postgres-password@localhost:6543/postgres'