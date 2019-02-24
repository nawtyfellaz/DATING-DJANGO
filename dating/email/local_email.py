DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jeloblistest@gmail.com' # sendgrid
EMAIL_HOST_PASSWORD ='Jeloblisvent1.'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Dating <info@dating.com>'
BASE_URL = '127.0.0.1:8000'

MANAGERS = (
    ('Jeremiah David', "jeremiahedavid@gmail.com"),
)

ADMINS = MANAGERS