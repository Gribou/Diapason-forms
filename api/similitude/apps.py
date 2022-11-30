from django.apps import AppConfig


class SimilitudeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'similitude'
    verbose_name = "Fiches Similitudes d'Indicatifs"

    def ready(self):
        import similitude.signals
