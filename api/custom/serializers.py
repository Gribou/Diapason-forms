from rest_framework import serializers
from constance import config

from . import models


class CustomFieldSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = models.CustomField
        fields = ['row', 'order', 'type', 'slug', 'label', 'help_text', 'size',
                  'choices', 'attrs', 'required']

    def get_choices(self, obj):
        return [item.label for item in obj.choices.choices.all()] if obj.choices is not None else []


class CustomFormSerializer(serializers.ModelSerializer):
    fields = CustomFieldSerializer(many=True)

    class Meta:
        model = models.CustomForm
        fields = ['title', 'slug', 'fields', 'description', 'send_email_to']


class FormCategorySerializer(serializers.ModelSerializer):
    forms = serializers.SerializerMethodField()

    class Meta:
        model = models.FormCategory
        fields = ['label', 'show_in_toolbar', 'forms']

    def get_forms(self, obj):
        result = []
        if config.SHOW_FNE and obj.include_fne:
            result.append(
                {"title": "Nouvelle FNE", "is_fne": True})
        if config.SHOW_SIMI and obj.include_simi:
            result.append(
                {"title": "Nouvelle Similitude d'Indicatifs", "is_simi": True})
        if config.SHOW_BROUILLAGE and obj.include_brouillage:
            result.append({
                "title": "Nouveau Brouillage", "is_brouillage": True
            })
        return result + [{"title": f.title, "slug": f.slug} for f in obj.forms.filter(enabled=True).all()]


def get_available_forms():
    return [
        {'slug': f.slug, 'title': f.title} for f in models.CustomForm.objects.filter(enabled=True)
    ]
