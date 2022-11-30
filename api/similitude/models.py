from django.db import models
from django.core.exceptions import ObjectDoesNotExist


from shared.models.form import FormOptions, AbstractForm, AbstractAction, AbstractRedactor
from shared.safetycube.utils import is_safetycube_enabled
from shared.models.investigator import AbstractCounter, AbstractPostIt
from . import model_managers
from .safetycube import SimiFormatter


class SimiAction(AbstractAction):
    pass


class SimiCounter(AbstractCounter):
    chart_name = "similitude"


class SimiOptions(FormOptions):
    action_class = SimiAction
    counter_class = SimiCounter
    safetycube_formatter_class = SimiFormatter
    short_form_name = "Similitude"
    long_form_name = "Fiche Similitude d'Indicatifs"
    long_form_name_plural = "Fiches Similitude d'Indicatifs"
    notification_permission = "be_notified_on_simi"
    detail_url_template = "similitude/show/"

    def is_safetycube_enabled(self):
        return is_safetycube_enabled()


class Simi(AbstractForm):
    objects = model_managers.PrefetchingSimiManager()
    options = SimiOptions()

    # override field from Form parent to use FneAction
    available_actions = models.ManyToManyField(
        SimiOptions.action_class,
        verbose_name="Actions possibles",
        default=None,
        blank=True,
        editable=False)

    with_incident = models.BooleanField("Avec incident", default=False)
    description = models.TextField("Description du problème rencontré")


class Redactor(AbstractRedactor):
    simi = models.ForeignKey(Simi,
                             on_delete=models.CASCADE,
                             related_name="redactors")


class Aircraft(models.Model):

    class Meta:
        verbose_name = "Aéronef"
        verbose_name_plural = "Aéronefs"

    callsign = models.CharField("Indicatif",
                                max_length=100,
                                null=False,
                                blank=False)
    strip = models.FileField('Photo du strip',
                             blank=True,
                             null=True,
                             max_length=250,
                             upload_to='simi/%Y/%m/strips/')
    simi = models.ForeignKey(Simi,
                             on_delete=models.CASCADE,
                             related_name='aircrafts')

    type = models.CharField("Type", max_length=4, null=True, blank=True)
    provenance = models.CharField(
        "Provenance", max_length=4, null=True, blank=True)
    destination = models.CharField(
        "Destination", max_length=4, null=True, blank=True)
    position = models.CharField(
        "Position", max_length=250, null=True, blank=True)
    ssr = models.CharField("Code SSR", max_length=20,
                           default='', blank=True)
    fl = models.PositiveIntegerField("Niveau", null=True)


class SubData(models.Model):

    class Meta:
        verbose_name = "Données sub"

    parent_simi = models.OneToOneField(Simi,
                                       verbose_name="Fiche parente",
                                       on_delete=models.CASCADE,
                                       related_name="sub_data",
                                       default=None)
    inca_number = models.CharField("Numéro INCA",
                                   max_length=25,
                                   blank=True,
                                   null=True)

    def get_parent(self):
        try:
            return self.parent_simi
        except ObjectDoesNotExist:
            return None


class PostIt(AbstractPostIt):

    parent = models.ForeignKey(SubData,
                               on_delete=models.CASCADE,
                               related_name="postits")
