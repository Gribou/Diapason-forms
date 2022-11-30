from django.apps import AppConfig
from django_celery_beat.apps import BeatConfig
from django_celery_results.apps import CeleryResultConfig
from constance.apps import ConstanceConfig


class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shared'
    verbose_name = "Configuration"

    def ready(self):
        import shared.signals


BeatConfig.verbose_name = "Tâches - Planification"
CeleryResultConfig.verbose_name = "Tâches - Résultats"
ConstanceConfig.verbose_name = "Paramètres"
# prevent unecessary migration :
ConstanceConfig.default_auto_field = "django.db.models.AutoField"
