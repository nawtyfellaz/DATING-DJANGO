import os

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jeloblistest@gmail.com' # sendgrid
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Jeloblisvent1.')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Datings <info@dating.com>'
BASE_URL = 'https://www.dating.com'

MANAGERS = (
    ('Jeremiah David', "jeremiahedavid@gmail.com"),
)

ADMINS = MANAGERS