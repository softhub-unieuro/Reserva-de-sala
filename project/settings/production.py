from .base import *
import dj_database_url
import os

BASE_DATABASES = DATABASES


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}

# Em produção, DEBUG deve ser sempre False, a menos que forçado via ENV para teste rápido
DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

if ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

# Database
database_url = os.getenv("DATABASE_URL")

if not database_url:
    db_name = os.getenv("DB_NAME") or os.getenv("DB_DATABASE")
    db_user = os.getenv("DB_USER") or os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if all([db_name, db_user, db_password, db_host, db_port]):
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

if database_url:
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,
            ssl_require=os.getenv("DB_SSL_REQUIRE", "False") == "True",
        )
    }
else:
    DATABASES = BASE_DATABASES

# Configurações de Segurança
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", False)
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", SECURE_SSL_REDIRECT)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", SECURE_SSL_REDIRECT)
SECURE_BROWSER_XSS_FILTER = env_bool("SECURE_BROWSER_XSS_FILTER", True)
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0" if not SECURE_SSL_REDIRECT else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", SECURE_SSL_REDIRECT)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", SECURE_SSL_REDIRECT)

# Arquivos Estáticos (WhiteNoise)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'