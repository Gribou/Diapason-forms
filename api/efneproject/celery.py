import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab
from celery.signals import task_failure
from datetime import datetime
from pytz import timezone

from shared.tasks import refresh_safetycube_for_all, clean as generic_clean, notify_investigators, clean_orphaned_media
from shared.email import mail_admins

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "efneproject.settings")

app = Celery('efneproject')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@task_failure.connect
def notify_admin_on_task_failure(**kwargs):
    if not settings.DEBUG:
        subject = "ERREUR : Tâche {sender.name} ({task_id}): {exception}".format(
            **kwargs)
        message = "Task {sender.name} with id {task_id} raised exception : {exception!r}\nTask was called with args: {args} kwargs: {kwargs}.The contents of the full traceback was:\n{einfo}".format(
            **kwargs)
        mail_admins(subject, message)


FORM_MODELS = [
    ('efne', 'Fne'),
    ('similitude', 'Simi'),
    ('brouillage', 'Brouillage')
]


@app.task
def clean():
    return [generic_clean(app_label, model_name) for app_label, model_name in FORM_MODELS] + [clean_orphaned_media()]


@app.task
def notify():
    return [notify_investigators(app_label, model_name) for app_label, model_name in FORM_MODELS]


@app.task
def refresh_safetycube():
    safetycube_models = [('efne', 'Fne'),
                         ('similitude', 'Simi')]
    return [refresh_safetycube_for_all(app_label, model_name) for app_label, model_name in safetycube_models]


app.conf.beat_schedule = {
    'clean_night': {
        "task": "efneproject.celery.clean",
        "schedule": crontab(minute=5, hour=4)
    },
    'clean_day': {
        "task": "efneproject.celery.clean",
        "schedule": crontab(minute=5, hour=13, nowfun=lambda: datetime.now(timezone('Europe/Paris')))
        # 13h05 locales
    },
    'notify': {
        "task": "efneproject.celery.notify",
        "schedule": crontab(minute=5)
    },
    #     'refresh_safetycube': {
    #         "task": "efneproject.celery.refresh_safetycube",
    #         "schedule": 3600.0  # once per hour
    #     }
}
