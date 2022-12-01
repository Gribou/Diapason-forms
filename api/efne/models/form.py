from django.db import models
from django.contrib.auth import get_user_model

from shared.models.form import FormOptions, AbstractForm, AbstractAction, AbstractRedactor
from shared.safetycube.utils import is_safetycube_enabled
from shared.models.investigator import AbstractCounter
from .. import model_managers
from ..safetycube import FneFormatter
from .config import TechAction, TechEventType, EventType


class FneAction(AbstractAction):
    pass


class FneCounter(AbstractCounter):
    chart_name = "fne"


class FneOptions(FormOptions):
    action_class = FneAction
    counter_class = FneCounter
    safetycube_formatter_class = FneFormatter
    short_form_name = "FNE"
    long_form_name = "Fiche de Notification d'Evènement"
    long_form_name_plural = "Fiches de Notification d'Evènement"
    notification_permission = 'be_notified_on_fne'
    detail_url_template = "fne/show/"

    def is_safetycube_enabled(self):
        return is_safetycube_enabled()


class Fne(AbstractForm):
    objects = model_managers.PrefetchingFneManager()
    options = FneOptions()

    # override field from Form parent to use FneAction
    available_actions = models.ManyToManyField(
        FneOptions.action_class,
        verbose_name="Actions possibles",
        default=None,
        blank=True,
        editable=False)

    secteur = models.CharField('Secteur',
                               max_length=25,
                               default='',
                               blank=True)
    position = models.CharField('Position',
                                max_length=25,
                                null=False, blank=False)
    regroupement = models.CharField('Regroupement',
                                    max_length=25,
                                    null=False, blank=False)
    lieu = models.CharField("Lieu de l'évènement",
                            max_length=100,
                            default='',
                            blank=True)
    isp = models.BooleanField("Instruction", default=False)

    event_types = models.ManyToManyField(EventType,
                                         verbose_name="Types d'évènements",
                                         default=None,
                                         blank=True)

    description = models.TextField("Description de l'évènement")
    drawing = models.ImageField('Schéma descriptif', blank=True,
                                null=True, max_length=250, upload_to='fne/%Y/%m/drawings/')

    tech_event = models.ManyToManyField(
        TechEventType,
        verbose_name="Types d'évènements techniques",
        default=None,
        blank=True)
    tech_actions_done = models.ManyToManyField(
        TechAction, verbose_name="Actions entreprises", default=None, blank=True)

    @property
    def event_type_list(self):
        return "/".join([e.name for e in self.event_types.all()])

    @property
    def zones(self):
        try:
            return "".join(self.redactors.values_list("team__zone__short_name", flat=True).distinct().all()) or None
        except:
            pass
    zones.fget.short_description = "Zones"


class Redactor(AbstractRedactor):
    role = models.CharField("Rôle", max_length=25)
    fne = models.ForeignKey(Fne,
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
                             upload_to='fne/%Y/%m/strips/')
    fne = models.ForeignKey(Fne,
                            on_delete=models.CASCADE,
                            related_name='aircrafts')


class CdsReport(models.Model):

    class Meta:
        verbose_name = "CR CDS"

    parent_fne = models.OneToOneField(Fne,
                                      verbose_name="FNE parente",
                                      on_delete=models.CASCADE,
                                      related_name='cds_report',
                                      default=None)
    com_cds = models.TextField("Commentaires Chef de Salle",
                               default='',
                               blank=True)
    rex_cds = models.BooleanField("REX Chef de Salle", default=False)
    notif_rpo = models.BooleanField("Notification RPO", default=False)
    cpi = models.BooleanField("Constat Préalable d'Infraction", default=False)


class Attachment(models.Model):
    class Meta:
        verbose_name = "Pièce jointe"
        verbose_name_plural = "Pièces jointes"

    parent = models.ForeignKey(
        Fne, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField("Pièce jointe", max_length=250,
                            upload_to="fne/%Y/%m/attachments/")
    author = models.ForeignKey(get_user_model(),
                               related_name="%(app_label)s_attachments",
                               on_delete=models.SET_NULL,
                               null=True)
