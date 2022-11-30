from shared.populate.populate import get_status_object, get_group_object

from .. import models
from . import config_demo


def populate_demo(verbose=True):
    # force creation of interference types if not exist
    if not models.InterferenceType.objects.exists():
        for rank, i in enumerate(config_demo.INTERFERENCE_TYPES):
            models.InterferenceType.objects.get_or_create(rank=rank, **i)
            if (verbose):
                print("Type de brouillage {}".format(i['name']))

    # force creation of available actions if not exist
    if not models.BrouillageAction.objects.exists():
        for current_status, graph in config_demo.BROUILLAGE_GRAPH.items():
            for current_group, actions in graph.items():
                for action in actions:
                    obj, created = models.BrouillageAction.objects.get_or_create(
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
