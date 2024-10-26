class LocalConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://postgres.your-tenant-id:your-super-secret-and-long-postgres-password@localhost:6543/postgres'