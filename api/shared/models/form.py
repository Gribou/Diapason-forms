from django.db import models
from django.contrib.auth.models import Group
import uuid


from .. import model_managers
from .config import Team
from .investigator import SafetyCubeRef


class Status(models.Model):

    class Meta:
        verbose_name = 'Statut'
        verbose_name_plural = 'Statuts'

    label = models.CharField("Intitulé", max_length=25)
    is_draft = models.BooleanField(default=False)
    is_waiting = models.BooleanField(default=False)
    is_in_progress = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    is_to_be_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class AbstractAction(models.Model):
    objects = model_managers.PrefetchingActionManager()

    class Meta:
        abstract = True
        verbose_name = "Action possible"
        verbose_name_plural = "Graphe d'actions"
        ordering = ['rank', 'is_default',
                    'next_status__label', 'next_group__name']

    label = models.CharField("Intitulé", max_length=250, default="Action")
    rank = models.PositiveIntegerField("Ordre", default=0)
    current_status = models.ForeignKey(Status,
                                       related_name="%(app_label)s_graph_for_current",
                                       verbose_name="Statut actuel",
                                       on_delete=models.SET_NULL,
                                       blank=True,
                                       null=True)
    current_group = models.ForeignKey(Group,
                                      verbose_name="Responsable actuel",
                                      related_name="%(app_label)s_graph_for_current_group",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    next_status = models.ForeignKey(Status,
                                    related_name="%(app_label)s_graph_for_next",
                                    verbose_name="Prochain statut",
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True)
    next_group = models.ForeignKey(Group,
                                   verbose_name="Prochain responsable",
                                   related_name="%(app_label)s_graph_for_next_group",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    is_default = models.BooleanField("Par défaut", default=False)
    is_terminal = models.BooleanField("Terminale", default=False)
    is_complete = models.BooleanField(
        "Complète", default=None, null=True, blank=True)

    def __str__(self):
        return '{} : {}/{} -> {}/{}'.format(
            self.label,
            self.current_status.label if self.current_status else None,
            self.current_group.name if self.current_group else None,
            self.next_status.label if self.next_status else None,
            self.next_group.name if self.next_group else None)


class FormOptions:
    short_form_name = "Formulaire"
    long_form_name = "Formulaire"
    long_form_name_plural = "Formulaires"
    action_class = AbstractAction

    def is_safetycube_enabled(self):
        return False


class AbstractForm(models.Model):
    options = FormOptions()

    class Meta:
        abstract = True
        verbose_name = "Formulaire"
        verbose_name_plural = "Formulaires"
        ordering = ['event_date']

    def __str__(self):
        return "{}".format(self.creation_date)

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.ForeignKey(Status,
                               verbose_name="Statut",
                               related_name="%(app_label)s",
                               on_delete=models.SET_NULL,
                               null=True)
    assigned_to_group = models.ForeignKey(Group,
                                          verbose_name="Attribué à",
                                          related_name="%(app_label)s",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True)
    assigned_to_person = models.CharField("Responsable",
                                          blank=True,
                                          null=True,
                                          max_length=25)
    keywords = models.CharField(
        "Mots-clés", max_length=250, null=True, blank=True,
        help_text="Eléments complémentaires pour aider à la catégorisation de la fiche. Renseignés par les utilisateurs analysant la fiche")
    creation_date = models.DateTimeField('Date de création', auto_now_add=True)
    update_date = models.DateTimeField('Date de mise à jour', auto_now=True)
    event_date = models.DateTimeField(
        "Date de l'évènement", null=False, blank=False)

    # this field needs to be overriden with a non-abstract Action class
    available_actions = models.ManyToManyField(
        FormOptions.action_class,
        verbose_name="Actions possibles",
        default=None,
        blank=True,
        editable=False)
    should_notify = models.BooleanField("Devrait déclencher un notification",
                                        default=False)
    safetycube = models.ForeignKey(
        SafetyCubeRef, null=True, blank=True, related_name="parent_%(app_label)s",
        on_delete=models.SET_NULL, verbose_name="Référence SafetyCube")

    def apply_action_by_pk(self, next_status_pk, next_group_pk):
        self.status = Status.objects.get(pk=next_status_pk)
        if self.assigned_to_group is None or str(
                self.assigned_to_group.pk) != str(next_group_pk):
            self.assigned_to_person = None
        self.assigned_to_group = Group.objects.get(
            pk=next_group_pk) if next_group_pk else None
        self.save()

    def apply_action(self, action):
        self.status = action.next_status
        if self.assigned_to_group is None or self.assigned_to_group != action.next_group:
            self.assigned_to_person = None
        self.assigned_to_group = action.next_group
        self.save()

    def apply_default_action(self):
        default_action = self.available_actions.filter(is_default=True).first()
        if default_action:
            self.apply_action(default_action)

    def mark_as_done_if_able(self):
        # if an action with status 'done' is available, apply this action
        done_actions = self.available_actions.filter(next_status__is_done=True)
        if done_actions.exists():
            self.apply_action(
                done_actions.order_by('is_default').first())

    def is_default_action_available(self):
        return self.available_actions.filter(is_default=True).exists()

    def is_action_available(self, next_status_pk, next_group_pk):
        return self.available_actions.filter(
            next_status__pk=next_status_pk,
            next_group__pk=next_group_pk).exists()

    def update_available_actions(self):
        next_actions = self.options.action_class.objects.filter(
            current_status=self.status).filter(
                current_group=self.assigned_to_group)
        if not next_actions.exists():
            # if no actions available, look for actions with no group
            # (a group may have been set for a status which do not expect one)
            next_actions = self.options.action_class.objects.filter(
                current_status=self.status).filter(current_group__isnull=True)
        self.available_actions.set(next_actions)

    def serialize_for_notification(self):
        return {
            'event_date': self.event_date.strftime('%d/%m/%Y') if self.event_date else None,
            'description': self.description,
            'analysis_is_done': self.status.is_done,
            'redactors': [{'email': r.email} for r in self.redactors.all()],
            'assigned_to_group': {"name": self.assigned_to_group.name} if self.assigned_to_group else None,
            'sub_data': {
                'inca_number': self.sub_data.inca_number} if hasattr(self, 'sub_data') else None,
            'safetycube_ref': self.safetycube.reference if hasattr(self, 'safetycube') and self.safetycube is not None else None
        }


class AbstractRedactor(models.Model):
    class Meta:
        abstract = True
        verbose_name = "Rédacteur"
        verbose_name_plural = "Rédacteurs"

    fullname = models.CharField("Nom", max_length=100, null=False, blank=False)
    team = models.ForeignKey(Team,
                             related_name="%(app_label)s_redactors",
                             null=True,
                             on_delete=models.SET_NULL)
    email = models.CharField("Email", max_length=100, null=True, blank=True)
