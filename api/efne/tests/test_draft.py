from rest_framework import status
from constance.test import override_config
from django.core import mail
from django.utils import timezone

from api.tests.base import *
from api.tests.utils import generate_any_file, generate_photo_file, generate_base64_image
from efne.models import EventType, Fne
from efne.views import DraftFneViewSet
from shared.models.form import Status
from shared.models.config import group_is_investigator, group_is_validator

FNE_DATA = {
    'secteur': 'A',
    'position': 'P1',
    'regroupement': 'AB',
    'lieu': 'LFLA',
    'isp': False,
    'description': "Il s'est passé des trucs.",
    'drawing': generate_base64_image(),
    'redactors[0].fullname': "Machin",
    'redactors[0].role': 'PCR',
    'redactors[0].team': "3E",
    'redactors[1].fullname': "Truc",
    'redactors[1].role': "ECR",
    'redactors[1].team': "2E",
    'aircrafts[0].callsign': 'GPAVU',
    'aircrafts[0].strip': generate_photo_file(),
    'aircrafts[1].callsign': 'GPAPU',
    'aircrafts[1].strip': generate_photo_file(),
    'event_date': timezone.now()
}
TCAS_DATA = {
    "tcas_report.traffic_info": True,
    "tcas_report.pilote_min_distance": 2.3,
    "tcas_report.pilote_min_altitude": 1000,
    "tcas_report.aircrafts[0].callsign": "AFR1000",
    "tcas_report.aircrafts[0].contact_radio": True,
}


class FneDraftTest(ApiTestCase):
    url = "/api/fne/draft/"

    def setUp(self):
        super().setUp()
        self.fne_data = {
            'event_types[0]': EventType.objects.filter(name='Radio').values_list(
                'pk', flat=True).first(),
            'event_types[1]': EventType.objects.filter(name='Contrôle').values_list('pk', flat=True).first(),
            **FNE_DATA
        }

    def _detail_view(self):
        return DraftFneViewSet.as_view(actions={'put': 'update', 'get': 'retrieve'}, detail=True)

    def _list_view(self):
        return DraftFneViewSet.as_view(actions={'post': 'create'})

    def _create_fne(self, data=None, user=None):
        request = self.factory.post(self.url,
                                    data if data is not None else self.fne_data,
                                    format="multipart")
        if user:
            force_authenticate(request, user=user)
        response = self._list_view()(request)
        return response.data['uuid']

    @override_config(SHOW_FNE=False)
    def test_feature_disabled(self):
        '''endpoint should raise error if feature is disabled'''
        request = self.factory.post(self.url, self.fne_data,
                                    format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_create_draft(self):
        '''endpoint should create a new FNE object with draft status'''
        request = self.factory.post(self.url, self.fne_data,
                                    format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_success(response.status_code))
        uuid = response.data['uuid']
        self.assertTrue(Fne.objects.get(uuid=uuid).status.is_draft)

    def test_create_raise_if_description_missing(self):
        '''endpoint should raise error if description is not provided'''
        self.fne_data.pop('description')
        request = self.factory.post(self.url, self.fne_data,
                                    format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_update_draft(self):
        '''endpoint should update object data. Status should stay 'draft' '''
        uuid = self._create_fne()
        self.fne_data['status'] = Status.objects.filter(
            is_waiting=True).first()
        self.fne_data['description'] = "Nouvelle description"
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Fne.objects.get(
            uuid=uuid).description, "Nouvelle description")
        # status is always forced to draft
        self.assertTrue(Fne.objects.get(uuid=uuid).status.is_draft)

    def test_strip_delete_on_update(self):
        '''endpoint should delete existing strip if file nor url are provided'''
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertIsNotNone(fne.aircrafts.filter(
            callsign="GPAVU").first().strip.file)
        self.fne_data.pop('aircrafts[0].strip')
        self.fne_data['aircrafts[0].pk'] = fne.aircrafts.get(
            callsign="GPAVU").pk
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertFalse(fne.aircrafts.filter(
            callsign="GPAVU").first().strip.name)

    def test_strip_keep_on_update(self):
        '''endpoint should keep existing strip if url is provided but not file'''
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.fne_data.pop('aircrafts[0].strip')
        self.fne_data['aircrafts[0].pk'] = fne.aircrafts.get(
            callsign="GPAVU").pk
        self.fne_data['aircrafts[0].strip_url'] = "url/strip.png"
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertIsNotNone(fne.aircrafts.get(callsign="GPAVU").strip.file)

    def test_strip_update_on_update(self):
        '''endpoint should update existing strip if file is provided'''
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.fne_data['aircrafts[0].pk'] = fne.aircrafts.get(
            callsign="GPAVU").pk
        self.fne_data['aircrafts[0].strip'] = generate_photo_file(
            title="other.png")
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne.refresh_from_db()
        self.assertIn("other.png", fne.aircrafts.filter(
            callsign="GPAVU").first().strip.name)

    @override_config(HOSTNAME="apps.crnan")
    def test_get_draft_link(self):
        ''' endpoint should send email containing frontend url with uuid'''
        uuid = self._create_fne()
        request = self.factory.post(
            "{}{}/send_link/".format(self.url, uuid), {'to': 'redactor@apps.crnan'}, format="multipart")
        response = DraftFneViewSet.as_view(
            actions={'post': 'send_link'}, detail=True)(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[0].to, ['redactor@apps.crnan'])
        self.assertIn("http://apps.crnan/fne/show/{}".format(uuid),
                      mail.outbox[0].body)

    def test_read_draft_by_uuid(self):
        '''endpoint should return serialized form with this uuid'''
        uuid = self._create_fne()
        request = self.factory.get("{}{}/".format(self.url, uuid))
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(
            response.data['description'], "Il s'est passé des trucs.")

    def test_list_endpoint_is_forbidden(self):
        '''list endpoint should raise 403'''
        request = self.factory.get(self.url)
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))
        force_authenticate(request, user=self.qss_user)
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_handle_proceed_options(self):
        '''auto advance to validation if 'proceed' '''
        self.fne_data['options.proceed'] = 'true'
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertTrue(fne.status.is_waiting)
        self.assertTrue(group_is_validator(fne.assigned_to_group))

    def test_handle_bypass_validation_options_anonymous_user(self):
        '''do nothing special if 'bypass_validation' and no authenticated user'''
        self.fne_data['options.proceed'] = 'true'
        self.fne_data['options.bypass_validation'] = 'true'
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertTrue(fne.status.is_waiting)
        self.assertTrue(group_is_validator(fne.assigned_to_group))

    def test_handle_bypass_validation_options_validator_user(self):
        '''auto-validate if 'bypass_validation' and validator user'''
        self.fne_data['options.proceed'] = 'true'
        self.fne_data['options.bypass_validation'] = 'true'
        uuid = self._create_fne(user=self.cds_user)
        fne = Fne.objects.get(uuid=uuid)
        self.assertTrue(fne.status.is_done)
        self.assertTrue(group_is_validator(fne.assigned_to_group))

    def test_handle_bypass_validation_options_all_access_user(self):
        '''auto-transfer if 'bypass_validation' and all access user'''
        self.fne_data['options.proceed'] = 'true'
        self.fne_data['options.bypass_validation'] = 'true'
        uuid = self._create_fne(user=self.qss_user)
        fne = Fne.objects.get(uuid=uuid)
        self.assertTrue(fne.status.is_waiting)
        self.assertTrue(group_is_investigator(fne.assigned_to_group))

    def test_cds_report_on_create(self):
        '''a CDS report can be provided directly on draft creation'''
        self.fne_data['cds_report.com_cds'] = "C'est moi le chef"
        self.fne_data['cds_report.notif_rpo'] = True
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertEqual(fne.cds_report.com_cds, "C'est moi le chef")

    def test_cds_report_on_update(self):
        '''a CDS report can be on draft update'''
        uuid = self._create_fne()
        self.fne_data['cds_report.com_cds'] = "C'est moi le chef"
        self.fne_data['cds_report.notif_rpo'] = True
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne = Fne.objects.get(uuid=uuid)
        self.assertEqual(fne.cds_report.com_cds, "C'est moi le chef")

    def test_attachment_on_create(self):
        '''attachments can be provided directly on draft creation'''
        self.fne_data['attachments[0].file'] = generate_photo_file()
        self.fne_data['attachments[1].file'] = generate_any_file()
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertEqual(fne.attachments.count(), 2)

    def test_rejects_attachment_if_too_big(self):
        self.fne_data['attachments[0].file'] = generate_any_file(
            size=100*1024*1024)
        request = self.factory.post(
            self.url, self.fne_data, format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_tcas_report_mandatory_if_tcas_event(self):
        '''if event type contains 'TCAS', the tcas report must be provided'''
        self.fne_data['event_types[0]'] = EventType.objects.filter(
            is_tcas=True).values_list('pk', flat=True).first()
        request = self.factory.post(
            self.url, self.fne_data, format="multipart")
        response = self._list_view()(request)
        self.assertTrue(status.is_client_error(response.status_code))
        self.fne_data.update(TCAS_DATA)
        uuid = self._create_fne()
        fne = Fne.objects.get(uuid=uuid)
        self.assertEqual(fne.tcas_report.aircrafts.first().callsign, "AFR1000")

    def test_tcas_report_on_update(self):
        '''tcas report can be provided on update'''
        uuid = self._create_fne()
        self.fne_data.update(TCAS_DATA)
        request = self.factory.put("{}{}/".format(
            self.url, uuid), self.fne_data, format="multipart")
        response = self._detail_view()(request, uuid=uuid)
        self.assertTrue(status.is_success(response.status_code))
        fne = Fne.objects.get(uuid=uuid)
        self.assertEqual(fne.tcas_report.aircrafts.first().callsign, "AFR1000")
