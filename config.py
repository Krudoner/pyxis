import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def _bool(env_value, default=False):
    if env_value is None:
        return default
    return str(env_value).lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 4000))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    
    # Codificamos la contraseña para seguridad en la URL
    raw_password = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_PASSWORD = quote_plus(raw_password) if raw_password else ''
    
    TESTING = os.environ.get('FLASK_ENV') == 'testing'
    
    if TESTING:
        MYSQL_DB = os.environ.get('MYSQL_TEST_DB', 'abptest')
    else:
        MYSQL_DB = os.environ.get('MYSQL_DB', 'pyxis_dev')

    # LA SOLUCIÓN: Solo el parámetro ssl_ca. SQLAlchemy lo convertirá internamente 
    # en el diccionario SSL que PyMySQL necesita, activando la conexión segura.
    if MYSQL_HOST != 'localhost':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?ssl_ca=/etc/ssl/certs/ca-certificates.crt"
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = _bool(os.environ.get('SESSION_COOKIE_SECURE'), False)
    SESSION_COOKIE_HTTPONLY = _bool(os.environ.get('SESSION_COOKIE_HTTPONLY'), True)
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_SECURE = _bool(os.environ.get('REMEMBER_COOKIE_SECURE'), False)
