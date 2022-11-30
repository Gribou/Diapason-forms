from constance import config
from PIL import Image

from .export import render_file_as_pdf, encode_image
from .email import send_mail
from .models.investigator import KnownRedactors


def send_answer_to_redactors(uuid, form_model, request):
    form = form_model.objects.get(uuid=uuid)
    export_template = "{}/export/pdf.html".format(form_model._meta.app_label)
    attachments = _make_mail_attachments(form, request, export_template)
    email_context = {'form': form, 'answer': request.data.get(
        'answer', ''), 'form_name': form.options.short_form_name}
    try:
        provenance = request.user.email
    except:
        pass
    send_mail(
        email_context,
        "Réponse fiche du {}".format(form.event_date.strftime("%d/%m/%Y")),
        "shared/emails/answer_to_redactors.html",
        "shared/emails/answer_to_redactors.txt",
        [r.get('email') for r in request.data.get('redactors', []) if r.get('email', None)], provenance=provenance or config.EMAIL_ADMIN, files=attachments)


def _make_mail_attachments(form, request, export_template):
    images, attachments = _organize_attachments(
        form, request.data.get('attachments', []))
    export_context = {
        'anonymous': True,
        'pdf_export_header': config.PDF_EXPORT_HEADER,
        'safetycube_enabled': form.options.is_safetycube_enabled(),
        'form': form,
        'title': form.options.short_form_name,
        'full_form_name': form.options.long_form_name,
        'encoded_strips': [
            encode_image(a.strip)
            for a in form.aircrafts.all()
        ] if hasattr(form, 'aircrafts') else None,
        'encoded_attachments': images,
        'encoded_drawing': encode_image(form.drawing) if hasattr(form, 'drawing') and form.drawing else None,

    }
    pdf_file = render_file_as_pdf(export_template, export_context, request)
    pdf_file.name = _make_attachment_title(form)
    return [pdf_file, *attachments]


def _make_attachment_title(form):
    try:
        if form.options.is_safetycube_enabled() and form.safetycube.reference:
            return "{}.pdf".format(form.safetycube.reference)
    except:
        pass
    try:
        if form.sub_data.inca_number:
            return "INCA{}.pdf".format(form.sub_data.inca_number)
    except:
        pass
    return "{}.pdf".format(form.event_date.strftime("%Y%m%d"))


def _organize_attachments(form, attachment_data):
    images = []
    attachments = []
    included_pk = [a.get('pk') for a in attachment_data]
    if hasattr(form, "attachments"):
        for a in form.attachments.filter(pk__in=included_pk):
            try:
                img = Image.open(a.file)
                img.verify()
                images.append(encode_image(a.file))
            except:
                attachments.append(a.file.path)
    return images, attachments


def remember_redactors(redactors):
    for r in redactors:
        fullname = r.get('fullname', None)
        team = r.get('team', None)
        email = r.get('email', None)
        if fullname and email and team:
            KnownRedactors.objects.update_or_create(
                fullname=fullname.strip().lower(), email=email.lower(), team=team)


def serialize_answer_suggestion(form):
    redactors = []
    for r in form.redactors.all():
        display_name = "{}{}".format(r.fullname, " ({})".format(
            r.team.label) if r.email else "")
        suggestions = KnownRedactors.objects.filter(
            fullname=r.fullname.lower(), team=r.team.label)
        if r.email:
            suggestions = suggestions.exclude(email=r.email.lower())
        main_suggestion = r.email
        if not main_suggestion and suggestions.exists():
            main_suggestion = suggestions.first().email
        redactors.append({
            'fullname': r.fullname,
            'team': r.team.label,
            'display_name': display_name,
            'email': main_suggestion,
            'suggestions': [*([r.email] if r.email else [])] + [s.email for s in suggestions.all()]
        })
    return {
        'redactors': redactors or [{}]
    }
