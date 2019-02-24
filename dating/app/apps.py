INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External Apps
    'phonenumber_field',
    'localflavor',
    'django_countries',

    # Local Apps
    # 'questions.apps.QuestionsConfig',
    # 'newsletter.apps.NewsletterConfig',
    # 'jobs.apps.JobsConfig',
    # 'likes.apps.LikesConfig',
    # 'matches.apps.MatchesConfig',
    # 'profiles.apps.ProfilesConfig',
    # 'loan.apps.LoanConfig',
    # 'contact.apps.ContactConfig',
]

# PHONENUMBER_DEFAULT_REGION = 'ISO-3166-1 US'

AUTH_USER_MODEL = 'accounts.User' #changes the built-in user model to ours
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/login/'

PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'
PHONENUMBER_DEFAULT_REGION = 'E164'