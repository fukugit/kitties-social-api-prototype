class LocalConfig:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://{user}:{password}@{host}/{name}'.format(**{
        'user': 'postgres.your-tenant-id',
        'password': 'your-super-secret-and-long-postgres-password',
        'host': 'localhost:6543',
        'name': 'postgres'
    })

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://{user}:{password}@{host}/{name}'.format(**{
        'user': 'postgres.zvuhoviybhrsppmznzmk',
        'password': 'dSqJfrLHJucwLFtY',
        'host': 'aws-0-ap-northeast-1.pooler.supabase.com:6543',
        'name': 'postgres'
    })