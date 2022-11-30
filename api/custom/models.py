from django.db import models
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator
from random import randrange

FIELD_TYPES = [
    ('text-input', 'Champ Texte'),
    ('password', 'Champ Mot de passe'),
    ('checkbox', 'Case à cocher'),
    ('checkbox-group', 'Groupe de cases à cocher'),
    ('radio', 'Boutons radio'),
    ('button', 'Bouton seul'),
    ('button-group', 'Groupe de boutons'),
    ('select', 'Liste de sélection'),
    ('date', 'Champ Date'),
    ('time', 'Champ Heure'),
    ('datetime', 'Champ Date et Heure'),
    ('photo', 'Photo'),
    ('drawing', 'Schéma'),
    ('text', 'Texte explicatif'),
    ('alert', 'Information/Avertissement'),
    ('divider', 'Séparateur'),
    ('empty', 'Vide')
]
READONLY_TYPES = ['text', 'alert', 'divider', 'empty']


class FormCategory(models.Model):
    label = models.CharField("Intitulé", max_length=250)
    rank = models.PositiveIntegerField("Ordre", default=0)
    show_in_toolbar = models.BooleanField(
        "Afficher dans la barre d'outils", default=False)
    include_fne = models.BooleanField("Inclure les FNE", default=False)
    include_simi = models.BooleanField(
        "Inclure les Similitudes d'Indicatifs", default=False)
    include_brouillage = models.BooleanField(
        "Inclure les Brouillages", default=False)
    show_to_groups = models.ManyToManyField(
        Group, default=None, blank=True, related_name="related_forms",
        verbose_name="Montrer aux groupes",
        help_text="Si aucun groupe n'est sélectionné, cette catégorie sera visible par tous, y compris sans authentification")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["rank", "label"]

    def __str__(self):
        return self.label


class SelectionList(models.Model):
    name = models.CharField("Nom", max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Liste de choix"
        verbose_name_plural = "Listes de choix"
        ordering = ['name']


class SelectionItem(models.Model):
    label = models.CharField("Intitulé", max_length=250)
    order = models.PositiveIntegerField("Ordre", default=0)
    parent_list = models.ForeignKey(
        SelectionList, related_name="choices", on_delete=models.CASCADE)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Choix"
        verbose_name_plural = "Choix"
        ordering = ['order', 'label']
        unique_together = ['label', 'parent_list']


class CustomForm(models.Model):
    enabled = models.BooleanField(
        "Activé", default=False, help_text="Afficher ou cacher ce formulaire pour l'utilisateur")
    category = models.ForeignKey(
        FormCategory, related_name='forms', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    title = models.CharField("Titre", max_length=250)
    slug = models.SlugField("Identifiant", unique=True,
                            help_text="Sera utilisé pour générer l'URL du formulaire")
    description = models.TextField("Description", blank=True, null=True)
    send_email_to = models.CharField(
        "Adresse e-mail de destination", help_text="ou identifiant du champ contenant l'adresse de destination", max_length=250, null=True, blank=True)
    # TODO other type of actions on submit ?

    def __str__(self):
        return self.title

    @property
    def preview(self):
        rows = {}
        for field in self.fields.all():
            if field.row not in rows:
                rows[field.row] = []
            rows[field.row].append(field.slug)
        return '\n'.join(['{} : '.format(i) + ' - '.join(row) for i, row in rows.items()])
    preview.fget.short_description = "Aperçu"

    class Meta:
        verbose_name = "Formulaire"
        verbose_name_plural = "Formulaires"
        ordering = ['slug']


class CustomField(models.Model):
    form = models.ForeignKey(
        CustomForm, related_name='fields', on_delete=models.CASCADE)
    row = models.PositiveIntegerField("Rangée", default=0)
    order = models.PositiveIntegerField("Ordre", default=0)
    type = models.CharField(
        "Type de champ", choices=FIELD_TYPES, default='text-input', max_length=100)
    slug = models.SlugField(
        "Identifiant", blank=True, null=True,
        help_text="Nom de ce champ utilisé pour le traitement des données")
    required = models.BooleanField("Obligatoire", default=False)
    label = models.CharField("Intitulé", max_length=250, blank=True, null=True)
    help_text = models.TextField("Texte d'aide", null=True, blank=True)
    choices = models.ForeignKey(
        SelectionList, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Liste de choix", help_text="Pour les champs de type 'Liste de sélection', 'Boutons radio', 'Groupe de cases à cocher', 'Groupes de boutons'")
    size = models.PositiveIntegerField(
        "Largeur", null=True, blank=True, validators=[MaxValueValidator(12)],
        help_text="La largeur du formulaire est divisé en 12.<br/>Saisissez ici le nombre de 12e que ce champ doit occuper.<br/>Laissez vide pour que le champ utilise tout l'espace disponible.<br/>Saississez 0 pour que le champ n'occupe que l'espace nécessaire.")
    attrs = models.JSONField(
        "Attributs", null=True, blank=True, help_text="Format JSON. Seront passés à la balise HTML représentant le champ. Voir documentation pour des exemples.", default=dict)

    def __str__(self):
        return self.slug

    def is_readonly(self):
        return self.type in READONLY_TYPES

    def save(self, *args, **kwargs):
        # force slug creation if non is provided
        if self.slug is None:
            self.slug = "{}{}".format(self.type, randrange(10))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Champ de formulaire"
        verbose_name_plural = "Champs de formulaire"
        ordering = ['row', 'order', 'slug']
        unique_together = ['slug', 'form']
