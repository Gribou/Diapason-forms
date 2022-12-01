from django.db import models
from .. import constants
from .form import Fne


class TCASReport(models.Model):

    class Meta:
        verbose_name = 'CR TCAS'
        verbose_name_plural = 'CRs TCAS'

    parent_fne = models.OneToOneField(Fne,
                                      verbose_name="FNE parente",
                                      on_delete=models.CASCADE,
                                      related_name='tcas_report',
                                      default=None)

    pilote_min_distance = models.FloatField(
        "Distance mini donnée par le pilote (en NM)", default=0, blank=True)
    ctl_min_distance = models.FloatField(
        "Distance mini donnée par le contrôleur (en NM)",
        default=0,
        blank=True)
    pilote_min_altitude = models.FloatField(
        "Altitude mini donnée par le pilote (en ft)", default=0, blank=True)
    ctl_min_altitude = models.FloatField(
        "Altitude mini donnée par le contrôleur (en ft)",
        default=0,
        blank=True)
    traffic_info = models.BooleanField("Information de trafic", default=False)
    pilot_request = models.BooleanField("Demande du pilote", default=False)
    before_manoeuvre = models.BooleanField("Avant la manoeuvre",
                                           null=True,
                                           blank=True)
    pilot_action_required = models.BooleanField("Action du pilote justifiée",
                                                default=False)
    disrupted_traffic = models.BooleanField("Gestion du trafic perturbée",
                                            default=False)
    asr = models.BooleanField("ASR", default=False)
    safety_net = models.BooleanField("Filet de sauvegarde", default=False)


class TCASReportAircraft(models.Model):

    class Meta:
        verbose_name = "Aéronef"
        verbose_name_plural = "Aéronefs"

    callsign = models.CharField("Indicatif",
                                max_length=20,
                                default='',
                                blank=True)
    ssr = models.CharField("Code SSR", max_length=20, default='', blank=True)
    flight_phase = models.CharField("Phase de vol",
                                    max_length=150,
                                    choices=constants.FLIGHT_PHASES,
                                    default=constants.LEVEL)
    real_fl = models.PositiveIntegerField("Niveau réel", null=True)
    assigned_fl = models.PositiveIntegerField("Niveau assigné", null=True)
    is_origin = models.BooleanField("Origine", default=False)
    is_vfr = models.BooleanField("VFR", default=False)
    is_mil = models.BooleanField("Militaire", default=False)
    advisory_type = models.CharField("Type d'avis",
                                     max_length=2,
                                     choices=constants.TCAS_TYPES,
                                     default=constants.TA,
                                     null=True)
    contact_radio = models.BooleanField("Contact radio", default=True)
    parent_report = models.ForeignKey(TCASReport,
                                      on_delete=models.CASCADE,
                                      related_name='aircrafts',
                                      null=False)
