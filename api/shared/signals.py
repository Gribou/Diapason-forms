from functools import wraps
import traceback
from .models.config import group_is_investigator
from .tasks import notify_redactors


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw', None):
            return
        signal_handler(*args, **kwargs)
    return wrapper


def is_completeness_unknown(sender, instance):
    # one of attributes relevant to completeness have change
    # a graph check needs to be run
    if instance.id:
        try:
            previous = sender.objects.get(id=instance.id)
            if previous.current_status != instance.current_status or \
                previous.current_group != instance.current_group or \
                    previous.next_status != instance.next_status or \
                previous.next_group != instance.next_group or \
                previous.is_terminal != instance.is_terminal:
                return True
            return False
        except:
            traceback.print_exc()
            pass
    return True


@disable_for_loaddata
def mark_graph_as_unknown_on_change(sender, instance, **kwargs):
    # mark completeness as unknown for instance to trigger a graph check
    if is_completeness_unknown(sender, instance):
        mark_all_actions_as_unknown(sender, instance)


def mark_all_actions_as_unknown(sender, instance, **kwargs):
    queryset = sender.objects.exclude(is_complete__isnull=True)
    if instance is not None and instance.id is not None:
        queryset = queryset.exclude(id=instance.id)
    queryset.update(is_complete=None)


def check_graph(sender, **kwargs):
    has_error = False
    for action in sender.objects.all():
        if not action.is_terminal and not sender.objects.filter(
                current_status=action.next_status,
                current_group=action.next_group).exists():
            action.is_complete = False
            has_error = True
        else:
            action.is_complete = True
        action.save()
    return not has_error


@disable_for_loaddata
def update_available_actions(sender, instance, **kwargs):
    instance.update_available_actions()


@disable_for_loaddata
def update_should_notify_on_form_change(sender, instance, **kwargs):
    old_form = sender.objects.filter(pk=instance.pk).first()
    if (old_form is None
        or old_form.assigned_to_group != instance.assigned_to_group
        ) and instance.assigned_to_group is not None:
        instance.should_notify = True


def should_notify_redactors(sender, instance):
    redactors = [r.email for r in instance.redactors.all()
                 if r.email is not None]
    if redactors:
        # FIXME email should not be sent  when validator mark as done
        previous = sender.objects.filter(pk=instance.pk).first()
        if not instance.status.is_draft and previous is not None and (instance.assigned_to_group is None or group_is_investigator(instance.assigned_to_group)):
            # if report has been transfered from one group to another (group of investigators only)
            if previous.assigned_to_group is not None and instance.assigned_to_group is not None and previous.assigned_to_group != instance.assigned_to_group:
                return True
            # or if report status has been set to done by investigator (even if group has not changed)
            if not previous.status.is_done and instance.status.is_done and group_is_investigator(previous.assigned_to_group):
                return True
    return False


@disable_for_loaddata
def notify_progress_to_redactors(sender, instance, update_fields, **kwargs):
    # Notify redactors by email each time their fne changes status or assigned group
    # Email sending is done in background task
    if should_notify_redactors(sender, instance):
        notify_redactors.delay(
            instance.serialize_for_notification(), sender._meta.app_label, sender._meta.model.__name__)


@disable_for_loaddata
def update_counters(instance, sender, **kwargs):
    counter_model = sender.options.counter_class
    # do not count drafts
    if instance.status and not instance.status.is_draft:
        date = instance.event_date.date()
        for counters in counter_model.objects.filter(date=date).all():
            counters.remove(instance.pk)
        for r in instance.redactors.all():
            if r.team is not None and r.team.zone is not None:
                # Separated counts are kept for each team category (ex LFFF : E and W)
                counter, created = counter_model.objects.get_or_create(
                    date=date, category=r.team.zone.short_name)
                counter.add(instance.pk)
            else:
                # Remaining reports are counted here
                counter, created = counter_model.objects.get_or_create(
                    date=date, category="Autres")
                counter.add(instance.pk)
        # A global counter is kept
        # (the sum of all other counters may count one form multiple time)
        counter, created = counter_model.objects.get_or_create(
            date=date, category="Global")
        counter.add(instance.pk)
