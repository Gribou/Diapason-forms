import lorem
from random import choices, choice

from shared.models.form import Status
from shared.models.config import Team
from brouillage.models import Brouillage, InterferenceType, Redactor, Aircraft, SubData
from brouillage.constants import AIR
from api.tests.utils import generate_random_datetime, generate_uploaded_photo_file


def random_brouillage_args():
    return {
        'event_date': generate_random_datetime(),
        'status': Status.objects.filter(is_draft=True).first(),
        'interferences': choices(list(InterferenceType.objects.all()), k=2),
        'description': lorem.text(),
        'frequency': "123.450",
        'redactors': [{
            'fullname': 'Fullname', 'team': choice(list(Team.objects.all()))
        }],
        'aircrafts': [{
            'callsign': 'FTOTO', 'strip': generate_uploaded_photo_file(),
            'fl': 210, 'waypoint': 'CLM', 'distance': 25, 'bearing': 330, 'plaintiff': AIR
        }]
    }


def create_brouillage(data):
    complete_data = random_brouillage_args()
    complete_data.update(data)
    redactors = complete_data.pop('redactors')
    aircrafts = complete_data.pop('aircrafts')
    sub_data = complete_data.pop("sub_data", None)
    interferences = complete_data.pop('interferences')
    brouillage = Brouillage.objects.create(**complete_data)
    brouillage.interferences.set(interferences)
    for r in redactors:
        Redactor.objects.create(brouillage=brouillage, **r)
    for a in aircrafts:
        Aircraft.objects.create(brouillage=brouillage, **a)
    if sub_data:
        SubData.objects.create(parent=brouillage, **sub_data)
    brouillage.refresh_from_db()
    brouillage.save()  # force update of counters taking redactors into account
    return brouillage
