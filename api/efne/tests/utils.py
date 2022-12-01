import lorem
from random import choices, choice

from shared.models.form import Status
from shared.models.investigator import SafetyCubeRef
from shared.models.config import Team
from efne.models import Fne, EventType, Role, Redactor, Aircraft, SubData
from api.tests.utils import generate_uploaded_photo_file, generate_random_datetime


def random_fne_args():
    return {
        'event_date': generate_random_datetime(),
        'status': Status.objects.filter(is_draft=True).first(),
        'event_types': choices(list(EventType.objects.all()), k=2),
        'description': lorem.text(),
        'redactors': [{
            'fullname': 'Fullname', 'team': choice(list(Team.objects.all())),
            'role': choice((list(Role.objects.all())))
        }],
        'aircrafts': [{
            'callsign': 'FTOTO', 'strip': generate_uploaded_photo_file()
        }]
    }


def create_fne(data):
    complete_data = random_fne_args()
    complete_data.update(data)
    redactors = complete_data.pop('redactors')
    aircrafts = complete_data.pop('aircrafts')
    event_types = complete_data.pop('event_types')
    sub_data = complete_data.pop('sub_data', None)
    safetycube = complete_data.pop("safetycube", None)
    fne = Fne.objects.create(**complete_data)
    fne.event_types.set(event_types)
    for r in redactors:
        Redactor.objects.create(fne=fne, **r)
    for a in aircrafts:
        Aircraft.objects.create(fne=fne, **a)
    if sub_data:
        SubData.objects.create(parent_fne=fne, **sub_data)
    if safetycube:
        fne.safetycube = SafetyCubeRef.objects.create(**safetycube)
    fne.save()  # force update of counters taking redactors into account
    fne.refresh_from_db()
    return fne
