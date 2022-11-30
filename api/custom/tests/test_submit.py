from rest_framework import status
from django.core import mail

from api.tests.base import *
from api.tests.utils import generate_uploaded_photo_file, generate_base64_image
from custom.populate import populate
from custom.models import CustomForm, SelectionItem, CustomField, SelectionList
from custom.views import CustomFormViewSet


class CustomFormSubmitTest(ApiTestCase):
    url = "/api/custom/form/test/submit/"

    def setUp(self):
        super().setUp()
        populate(verbose=False)
        yes_no = SelectionList.objects.get(name="oui_non")
        one_to_five = SelectionList.objects.create(name="1_to_5")
        for i in range(1, 6):
            SelectionItem.objects.create(
                label=str(i), order=i, parent_list=one_to_five)
        self.form = CustomForm.objects.create(
            enabled=True, title="Formulaire de test", slug="test", send_email_to="to")
        CustomField.objects.create(
            form=self.form, type="text-input", slug="text")
        CustomField.objects.create(
            form=self.form, type="checkbox", slug="checkbox")
        CustomField.objects.create(
            form=self.form, type="select", slug="select", choices=yes_no)
        CustomField.objects.create(
            form=self.form, type="checkbox-group", slug="multichoice", choices=one_to_five)
        CustomField.objects.create(
            form=self.form, type="date", slug="date")
        CustomField.objects.create(
            form=self.form, type="time", slug="time")
        CustomField.objects.create(
            form=self.form, type="datetime", slug="datetime")
        CustomField.objects.create(form=self.form, type="photo", slug="photo")
        CustomField.objects.create(
            form=self.form, type="text-input", slug="to", required=True)
        self.form_data = {"to": "test_form@apps.crnan"}

    def _submit(self):
        request = self.factory.post(
            self.url, self.form_data, format="multipart")
        response = CustomFormViewSet.as_view(
            {"post": "submit"})(request, slug="test")
        return response

    def test_submit_form(self):
        '''submit endpoint should accept form data and send email'''
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test_form@apps.crnan"])
        self.assertEqual(len(mail.outbox[0].attachments), 0)

    def test_hardcoded_destination(self):
        '''email should be sent to address in 'send_email_to' attribute'''
        self.form.send_email_to = "other_address@apps.crnan"
        self.form.save()
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["other_address@apps.crnan"])

    def test_missing_destination(self):
        '''error should be sent if destination is not provided'''
        self.form.send_email_to = None
        self.form.save()
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))

        self.form.send_email_to = "text"
        self.form.save()
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))

    def test_required_field(self):
        '''endpoint should raise error if required field is not submitted'''
        self.form_data.pop("to")
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("to", response.data)

    def test_validate_text(self):
        '''text field value should escape special chars'''
        self.form_data['text'] = "<test>"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['text'], "&lt;test&gt;")

    def test_validate_boolean(self):
        '''checkbox field should convert value to boolean'''
        self.form_data['checkbox'] = "not a bool"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['checkbox'], False)

        self.form_data['checkbox'] = "true"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data['checkbox'], True)

    def test_validate_choice(self):
        '''select field should raise error if value not in choices'''
        self.form_data['select'] = "not a choice"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("select", response.data)

        self.form_data['select'] = "Oui"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["select"], "Oui")

    def test_validate_multichoice(self):
        '''multichoice field should raise error if any value is not in choices'''
        self.form_data['multichoice[0]'] = "1"
        self.form_data['multichoice[1]'] = "2"
        self.form_data['multichoice[2]'] = "not a choice"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("multichoice", response.data)

        self.form_data['multichoice[0]'] = "3"
        self.form_data['multichoice[1]'] = "4"
        self.form_data['multichoice[2]'] = "5"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["multichoice"], ["3", "4", "5"])

    def test_validate_date(self):
        '''date field should raise error if value is not a valid date'''
        self.form_data['date'] = "not a date"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("date", response.data)

        self.form_data['date'] = "2021-52-13"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("date", response.data)

        self.form_data['date'] = "2018-01-01"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["date"], "2018-01-01")

    def test_validate_time(self):
        '''time field should raise error if value is not a valid time'''
        self.form_data['time'] = "not a time"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("time", response.data)

        self.form_data['time'] = "26:32"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("time", response.data)

        self.form_data['time'] = "13:00"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["time"], "13:00")

    def test_validate_datetime(self):
        '''datetime field should raise error if value is not a valid datetime'''
        self.form_data['datetime'] = "not a datetime"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("datetime", response.data)

        self.form_data['datetime'] = "2021-52-13 13:00"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertIn("datetime", response.data)

        self.form_data['datetime'] = "2018-01-01 13:00"
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["datetime"], "2018-01-01 13:00")

    def test_validate_file(self):
        '''image field should raise error if value is not a file or a base64 file'''
        self.form_data['photo'] = generate_uploaded_photo_file()
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        # 'photo' file is not returned in response

        self.form_data['photo'] = generate_base64_image()
        response = self._submit()
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        # 'photo' file is not returned in response

        self.form_data['photo'] = "not a file"
        response = self._submit()
        self.assertTrue(status.is_client_error(response.status_code))
