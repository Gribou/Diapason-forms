from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from constance import config

from shared.models.investigator import AbstractPostIt
from .form import Fne


class SubData(models.Model):

    class Meta:
        verbose_name = "Données sub"

    parent_fne = models.OneToOneField(Fne,
                                      verbose_name="FNE parente",
                                      on_delete=models.CASCADE,
                                      related_name="sub_data",
                                      default=None)
    inca_number = models.CharField("Numéro INCA",
                                   max_length=25,
                                   blank=True,
                                   null=True)
    hn = models.CharField(
        "HN",
        null=True,
        blank=True,
        max_length=25)
    is_safety_event = models.BooleanField("Evènement sécurité", default=False)
    alarm_acknowledged = models.BooleanField("Rappel acquitté", default=False)

    def get_parent(self):
        try:
            return self.parent_fne
        except ObjectDoesNotExist:
            return None

    @property
    def has_warning(self):
        days_since = (timezone.now() - self.get_parent().event_date).days
        return config.SAFETY_EVENT_WARNING_DAYS if self.is_safety_event and days_since >= config.SAFETY_EVENT_WARNING_DAYS and days_since < config.SAFETY_EVENT_ALARM_DAYS else None

    @property
    def has_alarm(self):
        days_since = (timezone.now() - self.get_parent().event_date).days
        return config.SAFETY_EVENT_ALARM_DAYS if self.is_safety_event and days_since >= config.SAFETY_EVENT_ALARM_DAYS else None


class PostIt(AbstractPostIt):

    parent = models.ForeignKey(SubData,
                               on_delete=models.CASCADE,
                               related_name="postits")
