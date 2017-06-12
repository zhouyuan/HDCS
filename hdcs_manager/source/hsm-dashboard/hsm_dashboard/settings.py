
import logging
import os
import sys
import warnings

from hsm_dashboard import exceptions

warnings.formatwarning = lambda message, category, *args, **kwargs: \
                                '%s: %s' % (category.__name__, message)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = '/usr/bin'

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = None

if not SECRET_KEY:
    from horizon.utils import secret_key
    SECRET_KEY = secret_key.generate_key()

# SECRET_KEY = '_n&qt--*3^1r--*$j6tk0^9t1^j_%134mm2frw_!!@3b3v56@1'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

ALLOWED_HOSTS = [
                 '*',
                 ]

SITE_BRANDING = 'HSM Dashboard'

WEBROOT = '/hsm_ui'
LOGIN_URL = WEBROOT + '/auth/login/'
LOGOUT_URL = WEBROOT + '/auth/logout/'
# LOGIN_REDIRECT_URL can be used as an alternative for
# HORIZON_CONFIG.user_home, if user_home is not set.
# Do not set it to '/home/', as this will cause circular redirect loop
LOGIN_REDIRECT_URL = WEBROOT
MEDIA_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'static'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'hsm_dashboard.urls'

HORIZON_CONFIG = {
    'dashboards': ('hsm',),
    'default_dashboard': 'hsm',
    'user_home': None,
    'ajax_queue_limit': 10,
    'auto_fade_alerts': {
        'delay': 3000,
        'fade_duration': 1500,
        'types': ['alert-success', 'alert-info']
    },
    'help_url': "hsm_ui/hsm",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

# Set to True to allow users to upload images to glance via Horizon server.
# When enabled, a file form field will appear on the create image form.
# See documentation for deployment considerations.
HORIZON_IMAGES_ALLOW_UPLOAD = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'horizon.middleware.HorizonMiddleware',
    # 'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'horizon.context_processors.horizon',
    'hsm_dashboard.context_processors.openstack',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader'
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

less_binary = os.path.join(BIN_DIR, 'lessc')
scss_binary = os.path.join('/usr', 'local', 'bin', 'scss')
COMPRESS_PRECOMPILERS = (
    ('text/less', (less_binary + ' {infile} {outfile}')),
    ('text/scss', (scss_binary + ' {infile} {outfile}')),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'dashboard'
COMPRESS_CSS_HASHING_METHOD = 'hash'
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_OFFLINE = True

INSTALLED_APPS = (
    'hsm_dashboard',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    #'hsm_dashboard.dashboards.project',
    #'hsm_dashboard.dashboards.admin',
    'hsm_dashboard.dashboards.hsm',
    'openstack_auth',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = False

gettext_noop = lambda s: s
LANGUAGES = (
    ('en', gettext_noop('English')),
)
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True

OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'Member'

DEFAULT_EXCEPTION_REPORTER_FILTER = 'horizon.exceptions.HorizonReporterFilter'

try:
    from local.local_settings import *
except ImportError:
    logging.warning("No local_settings file found.")

# Add HORIZON_CONFIG to the context information for offline compression
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'HORIZON_CONFIG': HORIZON_CONFIG
}

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

# Deprecation for Essex/Folsom dashboard names; remove this code in H.
_renames = (
    ('horizon.dashboards.hsm', 'hsm_dashboard.dashboards.hsm'),
)

INSTALLED_APPS = list(INSTALLED_APPS)
_dashboards = list(HORIZON_CONFIG['dashboards'])

for old, new in _renames:
    if old in INSTALLED_APPS:
        warnings.warn('The "%s" package is deprecated. Please update your '
                      'INSTALLED_APPS setting to use the new "%s" package.\n'
                      % (old, new), Warning)
        INSTALLED_APPS[INSTALLED_APPS.index(old)] = new
    _old_name = old.split(".")[-1]
    if _old_name in HORIZON_CONFIG['dashboards'] and _old_name != "settings":
        _new_name = new.split(".")[-1]
        warnings.warn('The "%s" dashboard name is deprecated. Please update '
                      'your HORIZON_CONFIG["dashboards"] setting to use the '
                      'new "%s" dashboard name.\n' % (_old_name, _new_name),
                      Warning)
        _dashboards[_dashboards.index(_old_name)] = _new_name
HORIZON_CONFIG['dashboards'] = _dashboards
