""" Django settings for efneproject project. """
import os
from pathlib import Path
from shared.safetycube.constants import SAFETYCUBE_SITE_IDS

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY",
                       'very_very_bad_secret_key__CHANGE_VALUE_IN_.env_FILE')

if DEBUG:
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
else:
    ALLOWED_HOSTS = ['*']
    a_h_list = [
        a_h
        for a_h in os.getenv("ALLOWED_HOSTS", '').replace('"', '').split(' ')
    ] if os.getenv("ALLOWED_HOSTS", None) else []
    CSRF_TRUSTED_ORIGINS = a_h_list
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = ['https://{}'.format(a_h) for a_h in a_h_list]
    CORS_ORIGIN_WHITELIST.append('http://localhost')
    CSRF_COOKIE_HTTPONLY = False  # so that javascript can read it
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    # indispensable pour servir des fichiers media avec le bon protocole :
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_EXPOSE_HEADERS = ['Content-Disposition']

# racine de l'application
URL_ROOT = os.getenv("URL_ROOT", '/')
FORCE_SCRIPT_NAME = CSRF_COOKIE_PATH = LANGUAGE_COOKIE_PATH = SESSION_COOKIE_PATH = URL_ROOT

# Fichiers statiques (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_web'),
]
STATIC_URL = URL_ROOT + 'static/'
WHITENOISE_STATIC_PREFIX = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Fichiers enregistrés
MEDIA_URL = URL_ROOT + 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
FILE_UPLOAD_PERMISSIONS = 0o644

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", None)
if EMAIL_BACKEND:
    # Envoi de mail par serveur SMTP (internet DGAC)
    EMAIL_HOST = os.getenv("EMAIL_HOST", '')
    EMAIL_PORT = os.getenv("EMAIL_PORT", "")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", '')
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
else:
    # mock email sending in "sent_emails" directory
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# use CONSTANCE_CONFIG instead
ADMINS = [('Admin', os.getenv('EMAIL_ADMIN', None))]
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_ADMIN", "")
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # admin emails 'from'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Applications tierces
    'constance',
    'constance.backends.database',
    'rest_framework',
    'djoser',
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',

    # Applications eFNE
    'shared',
    'sso',
    'efne',
    'similitude',
    'brouillage',
    'custom',
    'api'
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sso.middleware.KeycloakMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'
                  ] + MIDDLEWARE
    INTERNAL_IPS = ['127.0.0.1']  # for debug toolbar
    INSTALLED_APPS += ['rest_framework.authtoken',
                       'debug_toolbar', 'django_extensions']
else:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'efneproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates_web'),
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.getenv("DB_NAME", os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv("DB_USER", ''),
        'PASSWORD': os.getenv("DB_PASSWORD", ''),
        'HOST': os.getenv("DB_HOST", ''),
        'PORT': os.getenv("DB_PORT", '')
    }
}

WSGI_APPLICATION = 'efneproject.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

AUTHENTICATION_BACKENDS = [
    'sso.authentication.KeycloakAuthorizationBackend',
    'django.contrib.auth.backends.ModelBackend'
]

LOGOUT_REDIRECT_URL = "admin:login"
LOGIN_REDIRECT_URL = "admin:index"

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_ADDITIONAL_FIELDS = {
    'atco_mode_select': [
        'django.forms.fields.ChoiceField', {
            'widget': 'django.forms.Select',
            'choices': (("CAUTRA", 'CAUTRA'), ("4F", "4F"))  # TODO 3E ?
        }
    ],
    'db_type_select': [
        'django.forms.fields.ChoiceField', {
            'widget': "django.forms.Select",
            'choices': (("SAFETYCUBE", "SafetyCube"), ("INCA", "INCA"))
        }
    ],
    'site_id_select': [
        'django.forms.fields.ChoiceField', {
            'widget': 'django.forms.Select',
            'choices': SAFETYCUBE_SITE_IDS
        }
    ]
}
CONSTANCE_CONFIG = {
    'EMAIL_ADMIN': (os.getenv('EMAIL_ADMIN', "root@localhost"),
                    "Adresse e-mail de l'administrateur"),
    'EMAIL_SUBJECT_PREFIX':
    ('[EFNE] ',
     'Préfixe ajouté aux sujets des emails envoyés automatiquement'),
    'WEBSITE_NAME': ("eFNE", "Nom d'affichage de l'application"),
    'HOSTNAME':
    (os.getenv("HOSTNAME", "www.example.com"),
     "Nom de domaine où l'application est hébergée (pour la génération de lien dans les emails envoyés automatiquement)."
     ),
    'DRAFT_OBSOLESCENCE_DELAY':
    (48, "Délai en heures au-delà duquel un brouillon est considéré obsolète",
     int),
    'CDS_OBSOLESCENCE_DELAY':
    (24,
     "Délai en heures au-delà duquel un formulaire en attente de validation est considéré obsolète",
     int),
    'TO_BE_DELETED_DELAY':
    (24,
     "Délai en heures au-delà duquel un formulaire traité peut être supprimé de la base de données",
     int),
    'SHOW_STATS': (False, "Rendre publiques les statistiques d'utilisation de l'application (ex : nombre de FNE saisies)", bool),
    'SHOW_FNE': (True, "Activer les fonctionnalités relatives aux FNE", bool),
    'SHOW_SIMI': (True, "Activer les fonctionnalités relatives aux fiches de Similitude d'Indicatifs", bool),
    'SHOW_BROUILLAGE': (True, "Activer les fonctionnalités relatives aux fiches Brouillage"),
    'ATCO_MODE': ("CAUTRA", 'Outil de contrôle utilisé (influence les champs présentés dans le formulaire FNE : strip par ex)',  "atco_mode_select"),
    'DB_TYPE': ("INCA", 'Base de données utilisée pour archiver les fiches', 'db_type_select'),
    'FNE_CDS_WARNING_ENABLED': (True, "Informer le rédacteur qu'il doit prévenir son CDS à l'enregistrement de sa FNE"),
    'SIMI_CDS_WARNING_ENABLED': (True, "Informer le rédacteur qu'il doit prévenir son CDS à l'enregistrement de sa fiche similitude"),
    'BROUILLAGE_CDS_WARNING_ENABLED': (True, "Informer le rédacteur qu'il doit prévenir son CDS à l'enregistrement de sa fiche brouillage"),
    'FNE_SAVE_BUTTON_LABEL': ("Envoyer au CDS", "Intitulé du bouton enregistrant une nouvelle FNE"),
    'SIMI_SAVE_BUTTON_LABEL': ("Envoyer au CDS", "Intitulé du bouton enregistrant une nouvelle fiche similitude"),
    'BROUILLAGE_SAVE_BUTTON_LABEL': ("Envoyer au CDS", "Intitulé du bouton enregistrant une nouvelle fiche brouillage"),
    'SAFETY_EVENT_WARNING_DAYS': (60, "Afficher un avertissement sur les évènements sécurité ayant eu lieu il y a plus de ce nombre de jours"),
    'SAFETY_EVENT_ALARM_DAYS': (85, "Afficher une alarme sur les évènements sécurité ayant eu lieu il y a plus de ce nombre de jours"),
    'GALLERY_URL': ("", "URL permettant d'accéder à une API photothèque : https://nom-de-domaine/api/gallery/ (cf module portail)"),
    'PDF_EXPORT_HEADER': ('<h2 style="margin-bottom: 20px;">Diapason</h2><h4>Généré avec eFNE</h4>', "Texte affiché en entête des exports PDF"),
    'KEYCLOAK_ENABLED': (False, "Utiliser l'authentification SSO avec un serveur Keycloak"),
    'KEYCLOAK_SERVER_URL': ("http://localhost:8080/auth/", "URL du serveur Keycloak"),
    'KEYCLOAK_REALM': ('master', 'Nom de royaume Keycloak'),
    'KEYCLOAK_CLIENT_ID': ("nutshell", 'Identifiant de client Keycloak de cette application'),
    'KEYCLOAK_CLIENT_SECRET': ("__secret__", "Secret de client Keycloak de cette application"),
    'SAFETYCUBE_URL': ("https://www.safety-portal.fr/XXX/", "Adresse de SafetyCube pour l'enregistrement des fiches"),
    'SAFETYCUBE_USERNAME': ("", "Identifiant de connexion du compte de service"),
    'SAFETYCUBE_PASSWORD': ("", "Mot de passe du compte de service"),
    'SAFETYCUBE_SITE_ID': (0, "Identifiant Safetycube du site", 'site_id_select'),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Envoi d'emails":
    ('EMAIL_ADMIN', 'EMAIL_SUBJECT_PREFIX', 'WEBSITE_NAME', 'HOSTNAME'),
    "FNE Formulaire de notification d'évènements": ('SHOW_FNE', 'FNE_CDS_WARNING_ENABLED', 'FNE_SAVE_BUTTON_LABEL', 'SAFETY_EVENT_WARNING_DAYS', 'SAFETY_EVENT_ALARM_DAYS'),
    "Fiches de similitude d'indicatifs": ('SHOW_SIMI', 'SIMI_CDS_WARNING_ENABLED', 'SIMI_SAVE_BUTTON_LABEL'),
    "Fiches brouillage": ('SHOW_BROUILLAGE', 'BROUILLAGE_CDS_WARNING_ENABLED', 'BROUILLAGE_SAVE_BUTTON_LABEL'),
    "Nettoyage automatique des formulaires":
    ('DRAFT_OBSOLESCENCE_DELAY', 'CDS_OBSOLESCENCE_DELAY',
     'TO_BE_DELETED_DELAY'),
    "Configuration générale": ('SHOW_STATS', 'ATCO_MODE', 'DB_TYPE',  'GALLERY_URL', 'PDF_EXPORT_HEADER'),
    "SSO Keycloak": ("KEYCLOAK_ENABLED", "KEYCLOAK_SERVER_URL", "KEYCLOAK_REALM", "KEYCLOAK_CLIENT_ID", 'KEYCLOAK_CLIENT_SECRET'),
    "SafetyCube": ("SAFETYCUBE_URL",  "SAFETYCUBE_USERNAME", "SAFETYCUBE_PASSWORD", "SAFETYCUBE_SITE_ID"),
}

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION':
    '1.0',
    'ALLOWED_VERSIONS': ['1.0'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':
    [  # 'rest_framework.authentication.SessionAuthentication'
        'sso.authentication.CSRFExemptSessionAuthentication', ],
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT':
    'json'
}

DJOSER = {
    'SERIALIZERS': {
        'current_user': 'api.serializers.CustomUserSerializer',
    }
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
        'rest_framework.authentication.TokenAuthentication'
    ]

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-FR'

# On utilise directement "UTC" pour que les FNE soient affichées avec les
# bonnes heures (pas de conversion à faire)
TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Paris'
TIME_INPUT_FORMATS = ('%H:%M', )

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", None)
CELERY_TASK_DEFAULT_QUEUE = os.getenv("CELERY_QUEUE", "efne")
# do not send task to queue if no broker, run task locally (blocking) :
CELERY_TASK_ALWAYS_EAGER = CELERY_BROKER_URL is None
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

SILENCED_SYSTEM_CHECKS = [
    "rest_framework.W001",  # no default pagination class
    "corsheaders.E013",  # for test container
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'shared.email.ConstanceAdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ["console"],
            "level": "DEBUG",
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

try:
    from efneproject.version import __version__
    VERSION_TAG = __version__
except:
    VERSION_TAG = "?"
