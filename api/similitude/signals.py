from django.dispatch.dispatcher import receiver
from django.db.models import signals

from .models import Simi, SimiAction
from shared.signals import mark_graph_as_unknown_on_change, update_should_notify_on_form_change, update_available_actions, update_counters, mark_all_actions_as_unknown, notify_progress_to_redactors, disable_for_loaddata


@receiver(signals.post_save,
          sender=SimiAction,
          dispatch_uid="rerun_simi_action_graph")
@disable_for_loaddata
def rerun_action_graph(sender, instance, **kwargs):
    # force available actions update on all forms according to new action graph
    for f in Simi.objects.all():
        f.update_available_actions()


signals.pre_save.connect(
    mark_graph_as_unknown_on_change,
    sender=SimiAction,
    dispatch_uid="mark_simi_graph_as_unknown_on_update")
signals.post_delete.connect(
    mark_all_actions_as_unknown, sender=SimiAction,
    dispatch_uid="mark_simi_graph_as_unknown_on_delete")

signals.pre_save.connect(update_should_notify_on_form_change,
                         sender=Simi,
                         dispatch_uid="update_should_notify_for_simi")
signals.pre_save.connect(
    notify_progress_to_redactors,
    sender=Simi, dispatch_uid="notify_progress_to_redactors")
signals.post_save.connect(
    update_counters, sender=Simi, dispatch_uid="update_simi_counters")
signals.post_save.connect(update_available_actions, sender=Simi,
                          dispatch_uid="update_avalaible_actions_for_simi")
