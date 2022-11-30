from django.db import models


class GroupDetail(models.Model):

    class Meta:
        permissions = (
            ('validator', 'Valide les formulaire'),
            ('investigator', 'Analyse les formulaires'),
            ('all_access', 'A accès à tous les formulaires'),
        )


class UserDetail(models.Model):

    class Meta:
        permissions = (
            ("be_notified_on_fne", "Etre notifié pour les FNE"),
            ("be_notified_on_simi", "Etre notifié pour les fiches similitudes"),
            ("be_notified_on_brouillage", "Etre notifié pour les fiches brouillage")
        )


def group_is_validator(group):
    return group.permissions.filter(codename='validator').exists()


def group_is_investigator(group):
    return group.permissions.filter(codename='investigator').exists()


def group_has_all_access(group):
    return group.permissions.filter(codename='all_access').exists()


def user_is_validator(user):
    return user.has_perm('shared.validator')


def user_is_investigator(user):
    return user.has_perm('shared.investigator')


def user_has_all_access(user):
    return user.has_perm('shared.all_access')


class Sector(models.Model):
    label = models.CharField("Intitulé", max_length=10, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Secteur"
        verbose_name_plural = "Secteurs"
        ordering = ("label", )


class SectorGroup(models.Model):
    label = models.CharField("Intitulé", max_length=10, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Regroupement"
        verbose_name_plural = "Regroupements"
        ordering = ("label", )


class Position(models.Model):
    label = models.CharField("Intitulé", max_length=10, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Position de contrôle"
        verbose_name_plural = "Positions de contrôle"
        ordering = ("label", )


class TeamZone(models.Model):
    short_name = models.CharField("Identifiant", max_length=2, unique=True)
    color = models.CharField("Couleur",
                             null=True,
                             blank=True,
                             max_length=10, help_text="ex : #")

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones (Equipes)"
        ordering = ("short_name",)

    def __str__(self):
        return self.short_name


class Team(models.Model):
    label = models.CharField("Intitulé", max_length=10, unique=True)
    zone = models.ForeignKey(
        TeamZone, verbose_name="Zone",
        on_delete=models.SET_NULL, blank=True, null=True,
        help_text="Est utilisé pour catégoriser les fiches. Par exemple, E/W pour les centres ayant des zones de qualification.")
    rank = models.PositiveIntegerField("Ordre", default=0)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ("rank", "label")
