import environ
env = environ.Env()
environ.Env.read_env()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot',
]

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://user:pass@localhost:5432/testdb')
}

TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN')