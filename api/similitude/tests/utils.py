import lorem
from random import choice

from shared.models.form import Status, SafetyCubeRef
from shared.models.config import Team
from similitude.models import Simi, Redactor, Aircraft, SubData
from api.tests.utils import generate_uploaded_photo_file, generate_random_datetime


def random_similitude_args():
    return {
        'event_date': generate_random_datetime(),
        'status': Status.objects.filter(is_draft=True).first(),
        'description': lorem.text(),
        'redactors': [{
            'fullname': 'Fullname', 'team': choice(list(Team.objects.all())),
        }],
        'aircrafts': [{
            'callsign': 'FTOTO', 'strip': generate_uploaded_photo_file(), 'type': 'B777',
            'provenance': 'LFRU', 'destination': 'LFQV', 'position': 'RESMI', 'ssr': '1234', 'fl': 200
        }]
    }


def create_similitude(data):
    complete_data = random_similitude_args()
    complete_data.update(data)
    redactors = complete_data.pop('redactors')
    aircrafts = complete_data.pop('aircrafts')
    sub_data = complete_data.pop("sub_data", None)
    safetycube = complete_data.pop("safetycube", None)
    simi = Simi.objects.create(**complete_data)
    for r in redactors:
        Redactor.objects.create(simi=simi, **r)
    for a in aircrafts:
        Aircraft.objects.create(simi=simi, **a)
    if sub_data:
        SubData.objects.create(parent_simi=simi, **sub_data)
    if safetycube:
        simi.safetycube = SafetyCubeRef.objects.create(**safetycube)
    simi.refresh_from_db()
    simi.save()  # force update of counters taking redactors into account
    return simi
