from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from ..models import config, form
from . import config_demo


def populate_demo(verbose=True):
    # force creation of user groups if not exist
    if not Group.objects.exists():
        for group in config_demo.GROUPS:
            g = dict(group)
            name = g.pop('name', None)
            obj, created = Group.objects.get_or_create(name=name)
            if g.get('is_validator', False):
                obj.permissions.add(
                    Permission.objects.get(codename='validator'))
            if g.get('is_investigator', False):
                obj.permissions.add(
                    Permission.objects.get(codename='investigator'))
            if g.get('has_all_access', False):
                obj.permissions.add(
                    Permission.objects.get(codename='all_access'))
            if verbose:
                print("Groupe {}".format(name))

    # force creation of user groups if not exist
    if not get_user_model().objects.exclude(is_superuser=True).exists():
        for username, group_name in config_demo.USERS.items():
            user = get_user_model().objects.create_user(username=username,
                                                        password=username)
            user.groups.add(Group.objects.get(name=group_name))
            if verbose:
                print("Utilisateur {} (Groupe {})".format(
                    username, group_name))

    # force creation of statuses if not exist
    if not form.Status.objects.exists():
        for status in config_demo.STATUS_LIST:
            form.Status.objects.get_or_create(**status)
            if verbose:
                print("Statut {}".format(status['label']))

    # force creation of teams if not exist
    if not config.Team.objects.exists():
        for zone_name in config_demo.ZONES:
            zone, _ = config.TeamZone.objects.get_or_create(
                short_name=zone_name)
            for team_index in range(0, config_demo.TEAM_COUNT_PER_ZONE):
                team, _ = config.Team.objects.get_or_create(
                    label="{}{}".format(team_index + 1, zone),
                    zone=zone,
                    rank=team_index)
                if verbose:
                    print("Equipe {}".format(team.label))

    # force creation of sectors if not exist
    if not config.Sector.objects.exists():
        for sector in config_demo.SECTORS:
            config.Sector.objects.get_or_create(label=sector)
            if verbose:
                print("Secteur {}".format(sector))

    # force creation of working positions if not exist:
    if not config.Position.objects.exists():
        for position in config_demo.CWP:
            config.Position.objects.get_or_create(label=position)
            if verbose:
                print("Position {}".format(position))

    # force creation of sector groups if not exist:
    if not config.SectorGroup.objects.exists():
        for r in config_demo.UCESO:
            config.SectorGroup.objects.get_or_create(label=r)
            if verbose:
                print("Regroupement {}".format(r))


def get_status_object(label):
    return form.Status.objects.filter(label=label).first() if label != "" else None


def get_group_object(name):
    return Group.objects.filter(name=name).first() if name != "" else None
