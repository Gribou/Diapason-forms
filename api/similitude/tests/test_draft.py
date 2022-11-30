from rest_framework import status
from constance.test import override_config
from django.core import mail
from django.utils import timezone

from api.tests.base import *
from api.tests.utils import generate_photo_file
from similitude.models import Simi
from similitude.views import DraftSimiViewSet

SIMI_DATA = {
    'description': "Il s'est passé des trucs.",
    'redactors[0].fullname': "Machin",
    'redactors[0].team': "3E",
    'redactors[1].fullname': "Truc",
    'redactors[1].team': "2E",
    'aircrafts[0].callsign': 'GPAVU',
    'aircrafts[0].strip': generate_photo_file(),
    'aircrafts[0].type': "C510",
    'aircrafts[0].provenance': "LFPM",
    'aircrafts[0].destination': "LFRU",
    'aircrafts[0].ssr': "1234",
    'aircrafts[0].fl': 320,
    'aircrafts[1].callsign': 'GPAPU',
    'event_date': timezone.now(),
}


class SimiDraftTest(ApiTestCase):
    url = "/api/similitude/draft/"

    def setUp(self):
        super().setUp()
        self.simi_data = {**SIMI_DATA}

    def _detail_view(self):
        return DraftSimiViewSet.as_view(actions={'put': 'update', 'get': 'retrieve'}, detail=True)

    def _list_view(self):
        return DraftSimiViewSet.as_view(actions={'post': 'create'})

    def _create_simi(self, data=None, user=None):
        request = self.factory.post(
            self.url,
            data if data is not None else self.simi_data,
            format="multipart")
        if user:
            force_authenticate(request, user=user)
        response = self._list_view()(request)
        return response.data['uuid']

    @override_config(SHOW_SIMI=False)
    def test_feature_disabled(self):
        '''endpoint should raise error if feature is disabled'''
        request = self.factory.post(self.url, self.simi_data,
                                    format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_draft(self):
        '''endpoint should create a new simi object with draft status'''
        request = self.factory.post(self.url, self.simi_data,
                                    format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        uuid = response.data['uuid']
        self.assertTrue(Simi.objects.get(uuid=uuid).status.is_draft)

    def test_strip_delete_on_update(self):
        '''endpoint should delete existing strip if file nor url are provided'''
        uuid = self._create_simi()
        simi = Simi.objects.get(uuid=uuid)
        self.assertIsNotNone(simi.aircrafts.filter(
            callsign="GPAVU").first().strip.file)
        self.simi_data.pop('aircrafts[0].strip')
        self.simi_data['aircrafts[0].pk'] = simi.aircrafts.get(
            callsign="GPAVU").pk
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.simi_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        simi.refresh_from_db()
        self.assertFalse(simi.aircrafts.filter(
            callsign="GPAVU").first().strip.name)

    def test_strip_keep_on_update(self):
        '''endpoint should keep existing strip if url is provided but not file'''
        uuid = self._create_simi()
        simi = Simi.objects.get(uuid=uuid)
        self.simi_data.pop('aircrafts[0].strip')
        self.simi_data['aircrafts[0].pk'] = simi.aircrafts.get(
            callsign="GPAVU").pk
        self.simi_data['aircrafts[0].strip_url'] = "url/strip.png"
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.simi_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        simi.refresh_from_db()
        self.assertIsNotNone(simi.aircrafts.get(callsign="GPAVU").strip.file)

    def test_strip_update_on_update(self):
        '''endpoint should update existing strip if file is provided'''
        uuid = self._create_simi()
        simi = Simi.objects.get(uuid=uuid)
        self.simi_data['aircrafts[0].pk'] = simi.aircrafts.get(
            callsign="GPAVU").pk
        self.simi_data['aircrafts[0].strip'] = generate_photo_file(
            title="other.png")
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.simi_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        simi.refresh_from_db()
        self.assertIn("other.png", simi.aircrafts.filter(
            callsign="GPAVU").first().strip.name)

    @override_config(HOSTNAME="apps.crnan")
    def test_get_draft_link(self):
        ''' endpoint should send email containing frontend url with uuid'''
        uuid = self._create_simi()
        request = self.factory.post(
            "{}{}/send_link/".format(self.url, uuid), {'to': 'redactor@apps.crnan'}, format="multipart")
        response = DraftSimiViewSet.as_view(
            actions={'post': 'send_link'}, detail=True)(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, ['redactor@apps.crnan'])
        self.assertIn("http://apps.crnan/similitude/show/{}".format(uuid),
                      mail.outbox[0].body)
