from adjudiCat.settings.common import *
import environ
# SECURITY WARNING: keep the secret key used in production secret!
env = environ.Env(  # <-- Updated!
    # set casting, default value
    DEBUG=(bool, False),
)


environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Opcions per el deploy no segures
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

#------Cambiar per fer el deploy de manera segura
#SESSION_COOKIE_SECURE = False
#CSRF_COOKIE_SECURE = False
#SECURE_SSL_REDIRECT = False


ALLOWED_HOSTS = ['0.0.0.0','nattech.fib.upc.edu','172.16.4.41','172.19.0.1', '172.17.0.1','[::1]', '127.0.0.1', 'localhost',]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
