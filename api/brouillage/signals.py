from django.dispatch.dispatcher import receiver
from django.db.models import signals

from shared.signals import mark_graph_as_unknown_on_change, mark_all_actions_as_unknown, update_should_notify_on_form_change, notify_progress_to_redactors, update_available_actions, update_counters, disable_for_loaddata
from .models import Brouillage, BrouillageAction


@receiver(signals.post_save,
          sender=BrouillageAction,
          dispatch_uid="rerun_brouillage_action_graph")
@disable_for_loaddata
def rerun_action_graph(sender, instance, **kwargs):
    for f in Brouillage.objects.all():
        f.update_available_actions()


signals.pre_save.connect(
    mark_graph_as_unknown_on_change,
    sender=BrouillageAction,
    dispatch_uid="mark_brouillage_graph_as_unknown_on_update")
signals.post_delete.connect(
    mark_all_actions_as_unknown, sender=BrouillageAction,
    dispatch_uid="mark_brouillage_graph_as_unknown_on_delete")

signals.pre_save.connect(update_should_notify_on_form_change,
                         sender=Brouillage,
                         dispatch_uid="update_should_notify_for_brouillage")
signals.pre_save.connect(
    notify_progress_to_redactors,
    sender=Brouillage, dispatch_uid="notify_progress_to_redactors")
signals.post_save.connect(
    update_available_actions, sender=Brouillage,
    dispatch_uid="update_avalaible_actions_for_brouillage")
signals.post_save.connect(
    update_counters, sender=Brouillage, dispatch_uid="update_brouillage_counters")
