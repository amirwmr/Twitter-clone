from .base import *  # noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="5zyrF5uTeVhAJLHC0IcHBj-qcLqaPcPghvDFQWvUUPD2ffgt4tU",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default=("mailhog"))
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "support@twitterapi.site"
DOMAIN = env("DOMAIN")
SITE_NAME = "twitter API"
