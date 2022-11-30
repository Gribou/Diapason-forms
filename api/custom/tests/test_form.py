from rest_framework import status
from django.contrib.auth.models import Group

from api.tests.base import *
from custom.populate import populate
from custom.models import CustomForm, FormCategory, CustomField, SelectionList
from custom.views import CustomFormViewSet, FormCategoryViewSet


class CustomFormPopulateTest(ApiTestCase):
    url = "/api/custom/form/"
    category_url = "/api/custom/category/"

    def setUp(self):
        super().setUp()
        populate(verbose=False)
        self.contact = CustomForm.objects.get(slug="contact")

    def test_contact_form_preview(self):
        f = CustomForm.objects.get(slug="contact")
        # preview of form
        self.assertTrue(f.preview.endswith("2 : body"))
        # all fields have a non empty slug
        self.assertTrue(all([e.slug is not None for e in f.fields.all()]))
        self.assertFalse(f.fields.exclude(type="empty").first().is_readonly())
        self.assertTrue(f.fields.filter(type="empty").first().is_readonly())

    def test_get_menu(self):
        '''endpoint should return forms organized as categories'''
        request = self.factory.get(self.category_url)
        response = FormCategoryViewSet.as_view(
            actions={'get': 'list'})(request)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'Défaut')
        self.assertTrue(response.data[0]['show_in_toolbar'])
        self.assertTrue(response.data[0]['forms'][0]['is_fne'])
        self.assertTrue(response.data[0]['forms'][1]['is_simi'])
        self.assertTrue(response.data[0]['forms'][2]['is_brouillage'])

    def test_menu_show_forms_in_categories(self):
        '''show forms in categories only if enabled'''
        cat = FormCategory.objects.create(label="New")
        self.contact.category = cat
        self.contact.save()
        request = self.factory.get(self.category_url)
        response = FormCategoryViewSet.as_view(
            actions={'get': 'list'})(request)
        self.assertEqual(len(response.data[1]['forms']), 0)

        self.contact.enabled = True
        self.contact.save()
        request = self.factory.get(self.category_url)
        response = FormCategoryViewSet.as_view(
            actions={'get': 'list'})(request)
        self.assertEqual(len(response.data[0]['forms']), 3)
        self.assertTrue(response.data[1]['label'], 'New')
        self.assertTrue(response.data[1]['forms'][0]['slug'], 'contact')

    def test_menu_show_categories_for_groups(self):
        '''show forms according to show_to_group attribute'''
        category = FormCategory.objects.create(label="New")
        category.show_to_groups.set([Group.objects.get(name="Sub Etudes")])
        category.save()
        self.contact.category = category
        self.contact.enabled = True
        self.contact.save()
        request = self.factory.get(self.category_url)
        response = FormCategoryViewSet.as_view(
            actions={'get': 'list'})(request)
        self.assertEqual(len(response.data), 1)
        request = self.factory.get(self.category_url)
        force_authenticate(request, self.etu_user)
        response = FormCategoryViewSet.as_view(
            actions={'get': 'list'})(request)
        self.assertEqual(response.data[1]['forms'][0]['slug'], 'contact')

    def test_get_disabled_form(self):
        '''endpoint should not return a disabled custom form by slug'''
        request = self.factory.get("{}contact/".format(self.url))
        response = CustomFormViewSet.as_view(
            actions={'get': 'retrieve'})(request, slug="contact")
        self.assertTrue(status.is_client_error(response.status_code))

    def test_get_form(self):
        '''endpoint should return a custom form by slug'''
        self.contact.enabled = True
        self.contact.save()
        request = self.factory.get("{}contact/".format(self.url))
        response = CustomFormViewSet.as_view(
            actions={'get': 'retrieve'})(request, slug="contact")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data['fields']), 5)
        self.assertEqual(response.data['send_email_to'], 'root@localhost')

    def test_selection_list_field(self):
        '''select field should provide its selection list'''
        self.contact.enabled = True
        self.contact.save()
        CustomField.objects.create(
            form=self.contact, row=3, type='select', slug='select', choices=SelectionList.objects.first())
        request = self.factory.get("{}contact/".format(self.url))
        response = CustomFormViewSet.as_view(
            actions={'get': 'retrieve'})(request, slug="contact")
        self.assertIn('Oui', response.data['fields'][5]['choices'])
        self.assertIn('Non', response.data['fields'][5]['choices'])
