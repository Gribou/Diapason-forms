from django.apps import AppConfig


class BrouillageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brouillage'
    verbose_name = "Fiches Brouillage"

    def ready(self):
        import brouillage.signals
