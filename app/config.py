from datetime import timedelta
import os 

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',"postgresql://username:password@localhost/db-name")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "secret-key"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
