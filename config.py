import os
from dotenv import load_dotenv
load_dotenv()

def _bool(env_value, default=False):
    if env_value is None:
        return default
    return str(env_value).lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    
    TESTING = os.environ.get('FLASK_ENV') == 'testing'
    
    if TESTING:
        MYSQL_DB = os.environ.get('MYSQL_TEST_DB', 'abptest')
    else:
        MYSQL_DB = os.environ.get('MYSQL_DB', 'pyxis_dev')

    # Configuración de SQLAlchemy con soporte para SSL obligatorio (TiDB Cloud)
    # Si estamos en producción o cloud, activamos SSL para evitar el error 1105
    mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # Si hay host remoto (no localhost), añadimos los parámetros de SSL requeridos por TiDB
    if MYSQL_HOST != 'localhost':
        SQLALCHEMY_DATABASE_URI = f"{mysql_url}?ssl_verify_cert=true"
    else:
        SQLALCHEMY_DATABASE_URI = mysql_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie security flags
    SESSION_COOKIE_SECURE = _bool(os.environ.get('SESSION_COOKIE_SECURE'), False)
    SESSION_COOKIE_HTTPONLY = _bool(os.environ.get('SESSION_COOKIE_HTTPONLY'), True)
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_SECURE = _bool(os.environ.get('REMEMBER_COOKIE_SECURE'), False)
