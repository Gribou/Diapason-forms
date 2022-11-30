from shared.populate.populate import get_status_object, get_group_object
from .. import models
from . import config_demo


def populate_demo(verbose=True):
    # force creation of event types if not exist
    if not models.EventType.objects.exists():
        for rank, evt in enumerate(config_demo.EVENTS):
            models.EventType.objects.get_or_create(rank=rank, **evt)
            if verbose:
                print("Type d'évènement {}".format(evt['name']))

    # force creation of tech event types if not exist
    if not models.TechEventType.objects.exists():
        for rank, evt in enumerate(config_demo.TECH_EVENTS):
            models.TechEventType.objects.get_or_create(rank=rank, **evt)
            if verbose:
                print("Type d'évènement technique {}".format(evt['name']))

    if not models.TechAction.objects.exists():
        for action in config_demo.TECH_ACTIONS:
            models.TechAction.objects.create(**action)
            if verbose:
                print("Action technique {}".format(action['name']))
        # add all available actions to all tech event types
        for evt in models.TechEventType.objects.all():
            evt.actions.set(models.TechAction.objects.all())

    # force creation of sectors if not exist
    if not models.Role.objects.exists():
        for role in config_demo.REDAC_TYPES:
            models.Role.objects.get_or_create(label=role)
            if verbose:
                print("Rôle {}".format(role))

    # force creation of available actions if not exist
    if not models.FneAction.objects.exists():
        for current_status, graph in config_demo.FNE_GRAPH.items():
            for current_group, actions in graph.items():
                for action in actions:
                    obj, created = models.FneAction.objects.get_or_create(
                        current_status=get_status_object(current_status),
                        current_group=get_group_object(current_group),
                        label=action.get("label", None),
                        is_default=action.get("is_default", False),
                        is_terminal=action.get("is_terminal", False),
                        next_status=get_status_object(
                            action.get("next_status", '')),
                        next_group=get_group_object(
                            action.get("next_group", '')))
                    if verbose:
                        print("Action {}".format(obj))
