from constance import config
from django.utils.safestring import mark_safe
from django.apps import apps

from .constants import SAFETYCUBE_FORMID
from .requests import make_session, create, update, get_status


class FormFormatter:

    def make_payload(self, form):
        return {
            "siteId": int(config.SAFETYCUBE_SITE_ID),
            "date": form.event_date.strftime("%Y-%m-%d"),
            "formId": SAFETYCUBE_FORMID,
            'title': self.make_title(form),
            "fields": [
                {'name': k, 'value': v} for k, v in self.make_fields(form).items() if v
            ]
        }

    def make_fields(self, form):
        raise NotImplementedError()

    def make_title(self, form):
        raise NotImplementedError()


def is_safetycube_enabled():
    return config.DB_TYPE == "SAFETYCUBE" and bool(config.SAFETYCUBE_USERNAME)


def get_pretty_safetycube_ref(form):
    if form.safetycube is not None:
        return mark_safe(u'<a href="{}" target="_blank">{} ({})</a>'.format(
            form.safetycube.url, form.safetycube.reference, form.safetycube.status or '?'))


def _get_ref_model():
    return apps.get_model(app_label="shared", model_name="SafetyCubeRef")


def send_to_safetycube(uuid, form_model):
    form = form_model.objects.get(uuid=uuid)
    form = create_in_safetycube(form, make_session())
    return "Form sent to SafetyCube : {}".format(form.safetycube.reference)


def batch_send_to_safetycube(uuid_list, form_model):
    session = make_session()
    result = []
    for uuid in uuid_list:
        form = form_model.objects.get(uuid=uuid)
        if form.safetycube and form.safetycube.reference:
            update_in_safetycube(form, session)
            result.append(
                "Form updated in SafetyCube : {}".format(form.safetycube.reference))
        else:
            form = create_in_safetycube(form, session)
            result.append(
                "Form saved in SafetyCube : {}".format(form.safetycube.reference))
    return "\n".join(result)


def create_in_safetycube(form, session):
    formatter = form.options.safetycube_formatter_class()
    payload = formatter.make_payload(form=form)
    data = create(session, payload)
    ref = _get_ref_model().objects.create(
        url=data['publicUrl'], reference=data['reference'], status="OPEN")
    form.safetycube = ref
    form.save()
    return form


def update_in_safetycube(form, session):
    reference = form.safetycube.reference
    formatter = form.options.safetycube_formatter_class()
    if not reference:
        raise ValueError("SafetyCube reference cannot be empty")
    payload = formatter.make_payload(form=form)
    update(session, reference, payload)
    if form.safetycube.status is None:
        form.safetycube.status = "OPEN"
        form.safetycube.save()


def batch_refresh_safetycube_status(uuid_list, form_model):
    session = make_session()
    result = []
    for uuid in uuid_list:
        form = form_model.objects.get(uuid=uuid)
        if form.safetycube and form.safetycube.reference:
            result = get_status(session, form.safetycube.reference)
            form.safetycube.status = result['status']
            form.safetycube.save()
            if result['status'].lower() == "closed":
                form.mark_as_done_if_able()
    return "\n".join(result)


def refresh_safetycube_status(uuid, form_model):
    session = make_session()
    form = form_model.objects.get(uuid=uuid)
    if form.safetycube and form.safetycube.reference:
        result = get_status(session, form.safetycube.reference)
        form.safetycube.status = result['status']
        form.safetycube.save()
        if result['status'].lower() == "closed":
            form.mark_as_done_if_able()
