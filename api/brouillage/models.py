from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from shared.models.form import FormOptions, AbstractForm, AbstractAction, AbstractRedactor
from shared.models.investigator import AbstractCounter, AbstractPostIt
from . import model_managers
from .constants import AIR_OR_GROUND


class InterferenceType(models.Model):
    name = models.CharField("Intitulé", max_length=100)
    rank = models.PositiveIntegerField("Ordre")

    class Meta:
        verbose_name = "Type de brouillage"
        verbose_name_plural = "Types de brouillage"
        ordering = ['rank', 'name']


class BrouillageAction(AbstractAction):
    pass


class BrouillageCounter(AbstractCounter):
    chart_name = "brouillage"


class BrouillageOptions(FormOptions):
    short_form_name = "Brouillage"
    long_form_name = "Fiche Brouillage"
    long_form_name_plural = "Fiches Brouillage"
    action_class = BrouillageAction
    counter_class = BrouillageCounter
    notification_permission = "be_notified_on_brouillage"
    detail_url_template = "brouillage/show/"


class Brouillage(AbstractForm):
    objects = model_managers.PrefetchingBrouillageManager()
    options = BrouillageOptions()

    available_actions = models.ManyToManyField(
        BrouillageOptions.action_class, verbose_name="Actions possibles", default=None, blank=True, editable=False)

    interferences = models.ManyToManyField(
        InterferenceType, verbose_name="Types de brouillage", default=None, blank=True)
    frequency = models.CharField("Fréquence", max_length=100)
    cwp = models.CharField("Position de contrôle",
                           max_length=100, null=True, blank=True)
    description = models.TextField("Commentaire")
    freq_unusable = models.BooleanField(
        "Fréquence inutilisable", default=False)
    traffic_impact = models.BooleanField("Impact sur le trafic", default=False)
    supp_freq = models.BooleanField(
        "Utilisation d'une fréquence supplétive", default=False)


class Redactor(AbstractRedactor):

    brouillage = models.ForeignKey(Brouillage,
                                   on_delete=models.CASCADE,
                                   related_name="redactors")


class Aircraft(models.Model):

    class Meta:
        verbose_name = "Aéronef"
        verbose_name_plural = "Aéronefs"

    callsign = models.CharField(
        "Indicatif", max_length=100, null=False, blank=False)
    strip = models.FileField('Photo du strip', blank=True, null=True,
                             max_length=250, upload_to='brouillage/%Y/%m/strips/')
    brouillage = models.ForeignKey(
        Brouillage, on_delete=models.CASCADE, related_name='aircrafts')
    fl = models.PositiveIntegerField("Niveau", null=True)
    waypoint = models.TextField("Balise", null=True, blank=True)
    distance = models.PositiveIntegerField(
        "Distance", null=True, blank=True)
    bearing = models.PositiveIntegerField("Relèvement", null=True, blank=True)
    plaintiff = models.CharField(
        "Plaignant", choices=AIR_OR_GROUND, null=True, blank=True, max_length=50)


class SubData(models.Model):
    class Meta:
        verbose_name = "Données sub"

    # is needed to keep the same model graph than other forms : form -> subdata -> postit

    parent = models.OneToOneField(Brouillage, verbose_name="Fiche parente",
                                  on_delete=models.CASCADE, related_name="sub_data", default=None)

    def get_parent(self):
        try:
            return self.parent
        except ObjectDoesNotExist:
            return None


class PostIt(AbstractPostIt):
    parent = models.ForeignKey(
        SubData, on_delete=models.CASCADE, related_name="postits")
