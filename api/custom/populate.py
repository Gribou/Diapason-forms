from constance import config
from . import models


def populate(verbose=True):
    # add Yes/No Selection list if not exist
    if not models.SelectionList.objects.filter(name="oui_non").exists():
        l = models.SelectionList.objects.create(name="oui_non")
        models.SelectionItem.objects.create(
            label="Oui", order=0, parent_list=l)
        models.SelectionItem.objects.create(
            label="Non", order=1, parent_list=l)
        if verbose:
            print("Liste de sélection Oui/Non")

    # add basic contact form as example
    if not models.CustomForm.objects.filter(slug="contact").exists():
        form = models.CustomForm.objects.create(
            enabled=False, title="Formulaire de contact",
            description="Envoyez un email à l'administrateur du site",
            slug="contact", send_email_to=config.EMAIL_ADMIN)
        models.CustomField.objects.create(
            form=form, row=1,
            type="text-input", label="Objet", slug="object")
        models.CustomField.objects.create(
            form=form, row=0, type="text-input", slug="from", label="Adresse e-mail de réponse", required=True)
        models.CustomField.objects.create(
            form=form, row=0, order=1, type="empty", size=2)
        models.CustomField.objects.create(
            form=form, row=0, order=2, size=0, type="photo", slug="photo", label="Photo")
        models.CustomField.objects.create(
            form=form, row=2, type="text-input", slug="body", label="Message", attrs={'multiline': True, 'rows': 6}, required=True)

    # add a default menu category
    if not models.FormCategory.objects.exists():
        models.FormCategory.objects.create(
            label="Défaut", show_in_toolbar=True, include_fne=True, include_simi=True, include_brouillage=True)
