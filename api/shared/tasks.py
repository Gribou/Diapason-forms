from django.apps import apps
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import FileField
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import timedelta
from constance import config
from celery import shared_task
import os
from itertools import chain


from .email import send_mail
from .safetycube.utils import batch_send_to_safetycube, batch_refresh_safetycube_status


def clean_orphaned_media():
    # https://www.algotech.solutions/blog/python/deleting-unused-django-media-files/
    all_models = apps.get_models()
    physical_files = set()
    db_files = set()
    # Get all files from the database
    for model in all_models:
        file_fields = []
        filters = Q()
        for f_ in model._meta.fields:
            if isinstance(f_, FileField):
                file_fields.append(f_.name)
                is_null = {'{}__isnull'.format(f_.name): True}
                is_empty = {'{}__exact'.format(f_.name): ''}
                filters &= Q(**is_null) | Q(**is_empty)
        # only retrieve the models which have non-empty, non-null file
        # fields
        if file_fields:
            files = list(chain(*model.objects.exclude(filters).values_list(
                *file_fields).distinct()))
            db_files.update(files)
    # Get all files from the MEDIA_ROOT, recursively
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root is not None:
        for relative_root, dirs, files in os.walk(media_root):
            for file_ in files:
                # Compute the relative file path to the media directory, so
                # it can be compared to the values from the db
                relative_file = os.path.join(
                    os.path.relpath(relative_root, media_root), file_)
                physical_files.add(relative_file)
    # Compute the difference and delete those files
    deletables = physical_files - db_files
    if deletables:
        for file_ in deletables:
            try:
                os.remove(os.path.join(media_root, file_))
            except:
                # ignore if file is not found
                pass
        # Bottom-up - delete all empty folders
        for relative_root, dirs, files in os.walk(media_root,
                                                  topdown=False):
            for dir_ in dirs:
                if not os.listdir(os.path.join(relative_root, dir_)):
                    os.rmdir(os.path.join(relative_root, dir_))


@shared_task
def check_graph(app_label, action_model_name, verbose=False):
    action_model = apps.get_model(
        app_label=app_label, model_name=action_model_name)
    has_error = False
    for action in action_model.objects.all():
        if not action.is_terminal and not action_model.objects.filter(
                current_status=action.next_status,
                current_group=action.next_group).exists():
            print("{} :\tPas d'action suivante - ERROR !!".format(action))
            has_error = True
            action.is_complete = False
        else:
            action.is_complete = True
            if verbose:
                if action.is_terminal:
                    print("{} :\taction terminale - OK".format(action))
                else:
                    print("{} :\taction suivante détectée - OK".format(action))
        action.save()
    return "Le graphe d'actions est complet." if not has_error else "Le graphe d'actions est INCOMPLET."


def _get_time_threshold(delay_in_hours):
    return timezone.now() - timedelta(hours=delay_in_hours)


@shared_task
def clean(app_label, model_name):
    form_model = apps.get_model(
        app_label=app_label, model_name=model_name)
    result = ""
    # delete non-sent drafts older than delay in settings
    obsolete_drafts = form_model.objects.filter(
        status__is_draft=True,
        event_date__lt=_get_time_threshold(
            config.DRAFT_OBSOLESCENCE_DELAY))
    result += "{} {} brouillons obsolètes vont être supprimées.".format(
        obsolete_drafts.count(), form_model.options.short_form_name)
    obsolete_drafts.delete()

    # transfer to qss all validated forms and non-validated forms older than delay in settings
    obsolete_to_be_validated = form_model.objects\
        .filter(assigned_to_group__permissions__codename='validator')\
        .filter(
            Q(status__is_done=True) | (Q(status__is_waiting=True) & Q(
                event_date__lt=_get_time_threshold(config.CDS_OBSOLESCENCE_DELAY))))
    result += "{} {} en attente par le CDS vont être envoyées à la QS.".format(
        obsolete_to_be_validated.count(),  form_model.options.short_form_name)
    for form in obsolete_to_be_validated.all():
        # if form is still "waiting", the default action may need to be applied multiple times
        # apply default action until the form is not assigned to a validator anymore (or no other default action)
        while form.assigned_to_group.permissions.filter(codename='validator').exists() and form.is_default_action_available():
            form.apply_default_action()
            form.refresh_from_db()

    # delete from database form marked as to be deleted (by validator or by investigator)
    to_be_deleted = form_model.objects.filter(
        status__is_to_be_deleted=True,
        event_date__lt=_get_time_threshold(
            config.TO_BE_DELETED_DELAY))
    result += "{} {} dont le traitement est terminé vont être supprimées.".format(
        to_be_deleted.count(),  form_model.options.short_form_name)
    to_be_deleted.delete()
    return result if len(result) > 0 else "Rien à nettoyer"


def notify_investigators(app_label, model_name):
    form_model = apps.get_model(app_label=app_label, model_name=model_name)
    result = ""
    users_to_notify = get_users_with_perm(
        form_model.options.notification_permission).filter(email__isnull=False, is_superuser=False)
    if users_to_notify.exists():
        list_url = "https://{}{}list".format(config.HOSTNAME,
                                             reverse_lazy('home'))
        detail_url = "https://{}{}{}".format(
            config.HOSTNAME, reverse_lazy('home'), form_model.options.detail_url_template)
        for user in users_to_notify.all():
            forms = form_model.objects.filter(
                should_notify=True, assigned_to_group__in=user.groups.all())
            if forms.exists():
                context = {
                    'forms': forms,
                    'site_name': config.WEBSITE_NAME,
                    'list_url': list_url,
                    'detail_url': detail_url,
                    'contact_mail': config.EMAIL_ADMIN,
                    'form_name': form_model.options.long_form_name,
                    'form_name_plural': form_model.options.long_form_name_plural,
                    'safetycube_enabled': form_model.options.is_safetycube_enabled(),
                }
                plural = "s" if forms.count() > 1 else ""
                subject = "{} nouvelle{} {}".format(
                    forms.count(), plural, form_model.options.long_form_name_plural if plural else form_model.options.long_form_name)
                send_mail(
                    context, subject,
                    "{}/emails/notify_investigators.html".format(
                        form_model._meta.app_label),
                    "{}/emails/notify_investigators.txt".format(
                        form_model._meta.app_label),
                    [user.email])
                result = "will send mail to {} ({})".format(
                    user.email, subject)
    else:
        result = "No user to notify"
    for form in form_model.objects.filter(should_notify=True).all():
        form.should_notify = False
        form.save()
    return result


@shared_task
def notify_redactors(serialized_form, app_label, model_name):
    template_html = "shared/emails/notify_redactors.html",
    template_txt = "shared/emails/notify_redactors.txt"
    form_model = apps.get_model(app_label=app_label, model_name=model_name)
    context = {
        'form': serialized_form,
        'form_name': form_model.options.long_form_name,
        'site_name': config.WEBSITE_NAME,
        'contact_mail': config.EMAIL_ADMIN,
    }
    subject = "Avancement de votre {} du {}".format(
        form_model.options.long_form_name, serialized_form['event_date'])
    redactors = [r.get('email', None) for r in serialized_form['redactors']
                 if r.get('email', None) is not None]
    send_mail(context, subject, template_html, template_txt, redactors)


def get_users_with_perm(perm_name):
    return get_user_model().objects.filter(
        Q(user_permissions__codename=perm_name) | Q(groups__permissions__codename=perm_name)).distinct()


@shared_task
def refresh_safetycube_for_all(app_label, model_name):
    form_model = apps.get_model(app_label=app_label, model_name=model_name)
    uuid_list = form_model.objects.filter(
        safetycube__reference__isnull=False).values_list('uuid', flat=True)
    batch_refresh_safetycube_status(uuid_list, form_model)
    return list(form_model.objects.filter(
        safetycube__reference__isnull=False).values_list('safetycube__reference', flat=True).all())


@shared_task
def send_all_to_safetycube(uuid_list, app_label, model_name):
    form_model = apps.get_model(app_label=app_label, model_name=model_name)
    batch_send_to_safetycube(uuid_list, form_model)
