class LocalConfig:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # localからdocker composeで起動するSupabaseをそのまま利用
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://{user}:{password}@{host}/{name}'.format(**{
        'user': 'postgres.your-tenant-id',
        'password': 'your-super-secret-and-long-postgres-password',
        'host': 'localhost:6543',
        'name': 'postgres'
    })
    S3_BUCKET_NAME = 'files_development'
    S3_ENDPOINT = 'https://zvuhoviybhrsppmznzmk.supabase.co/storage/v1/s3'
    S3_REGION = 'ap-northeast-1'
    S3_ACCESS_KEY = 'f18c1ed396721a4a52808f592024a613'
    S3_SECRET_KEY = 'dd1390807ec2100b1fbbcc99f8b21a3bef5fc71d974303275ad20d6834dff187'

    # 環境変数でmode=developmentを設定すれば利用可能
class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # the pet companyのprojectにあるリモートsupabaseを利用
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://{user}:{password}@{host}/{name}'.format(**{
        'user': 'postgres.zvuhoviybhrsppmznzmk',
        'password': 'dSqJfrLHJucwLFtY',
        'host': 'aws-0-ap-northeast-1.pooler.supabase.com:6543',
        'name': 'postgres'
    })
    S3_BUCKET_NAME = 'files_development'
    S3_ENDPOINT = 'https://zvuhoviybhrsppmznzmk.supabase.co/storage/v1/s3'
    S3_REGION = 'ap-northeast-1'
    S3_ACCESS_KEY = 'f18c1ed396721a4a52808f592024a613'
    S3_SECRET_KEY = 'dd1390807ec2100b1fbbcc99f8b21a3bef5fc71d974303275ad20d6834dff187'