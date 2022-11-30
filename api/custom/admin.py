from django.contrib import admin, messages
from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import json
import logging
import traceback

from shared.admin import ExtraButtonsMixin
from .serializers import CustomFormSerializer
from . import models

logger = logging.getLogger("django")


class SelectionItemInline(admin.TabularInline):
    model = models.SelectionItem


class SelectionListAdmin(admin.ModelAdmin):
    model = models.SelectionList
    list_display = ('name', 'get_preview')
    inlines = [SelectionItemInline]

    def get_preview(self, obj):
        preview = [i.label for i in obj.choices.all()]
        return preview[:75] + "..." if len(preview) > 75 else preview
    get_preview.short_description = "Aperçu"


class FormCategoryAdmin(admin.ModelAdmin):
    model = models.FormCategory
    list_display = ('label', 'include_fne', 'include_simi',
                    'include_brouillage', 'get_forms')
    filter_horizontal = ('show_to_groups', )

    def get_forms(self, obj):
        return ", ".join([f.title for f in obj.forms.all()])
    get_forms.short_description = "Formulaires personnalisés"


class CustomFieldInline(admin.StackedInline):
    model = models.CustomField
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                ('slug', 'required', 'form'),
                ('type', 'choices'),
                ('label', 'help_text',),
                ('row', 'order', 'size'),
                'attrs'
            ),
        }),
    )


class JsonImportForm(forms.Form):
    json_file = forms.FileField(label="Fichier")


class CustomFormAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    change_list_template = "custom/admin/changelist_with_extra_buttons.html"
    model = models.CustomForm
    list_display = ('title', 'slug', 'send_email_to', 'category', 'enabled')
    inlines = [CustomFieldInline]
    readonly_fields = ['preview']
    actions = ['export_as_json']
    fieldsets = (
        (None, {
            'fields': (
                ('slug', 'send_email_to', 'enabled'),
                ('title', 'category'),
                'description',
                'preview'
            ),
        }),
    )

    def get_extra_buttons(self):
        return [
            {'title': 'Importer JSON', 'path': 'import-json/',
                'method': self.import_json}
        ]

    def import_json(self, request):
        if request.method == "POST" and request.FILES:
            try:
                json_data = json.load(request.FILES["json_file"])
                for form_data in json_data:
                    fields = form_data.pop('fields')
                    fm = models.CustomForm.objects.create(**form_data)
                    if fields:
                        for f in fields:
                            models.CustomField.objects.create(form=fm, **f)
                self.message_user(request, "Formulaires importés")
            except Exception as e:
                logger.error(e)
                self.message_user(
                    request, "L'import de formulaire a échoué : {}".format(e),
                    level=messages.ERROR)
                traceback.print_exc()
            finally:
                return redirect('../')
        form = JsonImportForm()
        payload = {"form": form}
        return render(
            request, "custom/admin/json_form.html", payload
        )

    def export_as_json(self, request, queryset):
        data = CustomFormSerializer(
            queryset, many=True, context={'request': request}).data
        response = HttpResponse(json.dumps(data))
        response['Content-Disposition'] = 'attachment; filename={}.json'.format(
            self.model._meta)
        return response
    export_as_json.short_description = "Exporter au format JSON"


admin.site.register(models.SelectionList, SelectionListAdmin)
admin.site.register(models.CustomForm, CustomFormAdmin)
admin.site.register(models.FormCategory, FormCategoryAdmin)
