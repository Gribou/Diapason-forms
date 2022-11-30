from django.dispatch.dispatcher import receiver
from django.db.models import signals

from .models import Fne, FneAction, FneCounter
from shared.signals import mark_all_actions_as_unknown, mark_graph_as_unknown_on_change, update_should_notify_on_form_change, update_available_actions, notify_progress_to_redactors, disable_for_loaddata


@receiver(signals.post_save,
          sender=FneAction,
          dispatch_uid="rerun_fne_action_graph")
@disable_for_loaddata
def rerun_action_graph(sender, instance, **kwargs):
    # force available actions update on all forms according to new action graph
    for f in Fne.objects.all():
        f.update_available_actions()


signals.pre_save.connect(
    mark_graph_as_unknown_on_change,
    sender=FneAction,
    dispatch_uid="mark_fne_graph_as_unknown_on_update")
signals.post_delete.connect(
    mark_all_actions_as_unknown, sender=FneAction,
    dispatch_uid="mark_fne_graph_as_unknown_on_delete")

signals.pre_save.connect(
    update_should_notify_on_form_change,
    sender=Fne,
    dispatch_uid="update_should_notify_for_fne")
signals.pre_save.connect(
    notify_progress_to_redactors,
    sender=Fne, dispatch_uid="notify_progress_to_redactors")
signals.post_save.connect(
    update_available_actions, sender=Fne,
    dispatch_uid="update_avalaible_actions_for_fne")


@receiver(signals.post_save, sender=Fne, dispatch_uid="update_fne_counters")
@disable_for_loaddata
def update_fne_counters(sender, instance, **kwargs):
    # add fne to relevant counters and remove from all other counters
    # do not count drafts
    if instance.status and not instance.status.is_draft:
        date = instance.event_date.date()
        for counters in FneCounter.objects.filter(date=date).all():
            counters.remove(instance.pk)
        for r in instance.redactors.all():
            if r.role == "QSS":
                # Fne created by QSS are usually submitted in paper or from sources external to the local control room
                counter, created = FneCounter.objects.get_or_create(
                    date=date, category="QSS")
                counter.add(instance.pk)
            elif r.team is not None and r.team.zone is not None:
                # Separated counts are kept for each team category (ex : E and W)
                counter, created = FneCounter.objects.get_or_create(
                    date=date, category=r.team.zone.short_name)
                counter.add(instance.pk)
            else:
                # Remaining Fne are counted here
                counter, created = FneCounter.objects.get_or_create(
                    date=date, category="Autres")
                counter.add(instance.pk)
        # A global counter is kept
        # (the sum of all other counters may count one fne multiple time)
        counter, created = FneCounter.objects.get_or_create(
            date=date, category="Global")
        counter.add(instance.pk)
