import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Engine

load_dotenv()

# INTERCEPTOR GLOBAL: Atrapa cualquier intento de conexión a la base de datos
# y le inyecta el diccionario SSL nativo directamente a PyMySQL.
@event.listens_for(Engine, "do_connect")
def add_ssl_to_pymysql(dialect, conn_rec, cargs, cparams):
    host = os.environ.get('MYSQL_HOST', 'localhost')
    # Solo inyectamos el SSL si nos conectamos a TiDB (no en local)
    if host != 'localhost' and 'pymysql' in dialect.driver:
        cparams["ssl"] = {
            "ca": "/etc/ssl/certs/ca-certificates.crt",
            "check_hostname": False
        }

def _bool(env_value, default=False):
    if env_value is None:
        return default
    return str(env_value).lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 4000))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    
    # Contraseña codificada de forma segura
    raw_password = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_PASSWORD = quote_plus(raw_password) if raw_password else ''
    
    TESTING = os.environ.get('FLASK_ENV') == 'testing'
    
    if TESTING:
        MYSQL_DB = os.environ.get('MYSQL_TEST_DB', 'abptest')
    else:
        MYSQL_DB = os.environ.get('MYSQL_DB', 'pyxis_dev')

    # URL 100% limpia. El interceptor de arriba se encarga de todo el SSL
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = _bool(os.environ.get('SESSION_COOKIE_SECURE'), False)
    SESSION_COOKIE_HTTPONLY = _bool(os.environ.get('SESSION_COOKIE_HTTPONLY'), True)
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_SECURE = _bool(os.environ.get('REMEMBER_COOKIE_SECURE'), False)
