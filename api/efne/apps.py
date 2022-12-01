from django.apps import AppConfig


class EfneConfig(AppConfig):
    name = 'efne'
    verbose_name = "Fiches Notification d'Evènements"

    def ready(self):
        import efne.signals
