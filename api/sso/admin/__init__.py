from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple

from ..tasks import refresh_keycloak
from ..models import SSOConfig, SSOUserProfile
from shared.models import config


def refresh_realm(modeladmin, request, queryset):
    result = refresh_keycloak.delay()
    modeladmin.message_user(
        request,
        mark_safe("<a href='{}'>Tâche {} ajoutée à la file</a> ({})".format(
            reverse_lazy('admin:django_celery_results_taskresult_changelist'), result.task_id, result.status))
    )


refresh_realm.short_description = "Actualiser la configuration Keycloak"


class SSOConfigAdmin(admin.ModelAdmin):
    model = SSOConfig
    fields = ['well_known_oidc', 'public_key']
    readonly_fields = ['well_known_oidc', 'public_key']
    actions = [refresh_realm]

    def has_add_permission(self, request):
        # check if generally has add permission
        if SSOConfig.objects.exists():
            return False
        return super().has_add_permission(request)


class SSOProfileInline(admin.StackedInline):
    model = SSOUserProfile
    readonly_fields = ['sub', 'access_token', 'expires_before',
                       'refresh_token', 'refresh_expires_before']


class CustomUserAdmin(UserAdmin):
    inlines = [SSOProfileInline]
    list_display = ['username', 'email', 'get_groups',
                    'is_staff', 'is_sso',  'get_notifications', 'last_login']
    search_fields = ['username', 'email', 'groups__name']

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Groupes"

    def get_notifications(self, obj):
        # notifications are always disabled for superusers
        if obj.is_superuser:
            return ""
        result = []
        if obj.has_perm('shared.be_notified_on_fne'):
            result.append("FNE")
        if obj.has_perm('shared.be_notified_on_simi'):
            result.append("Similitudes")
        if obj.has_perm('shared.be_notified_on_brouillage'):
            result.append("Brouillage")
        return ', '.join(result)

    get_notifications.short_description = "Notifications"

    def is_sso(self, obj):
        try:
            return obj.sso_profile.sub is not None
        except:
            return False
    is_sso.boolean = True
    is_sso.short_description = "SSO"


class GroupAdminForm(ModelForm):
    # edit user set from group admin
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class CustomGroupAdmin(GroupAdmin):
    list_display = [
        'name', 'is_validator', 'is_investigator', 'has_all_access'
    ]
    form = GroupAdminForm

    def is_validator(self, obj):
        return config.group_is_validator(obj)

    is_validator.short_description = "Validateur"
    is_validator.boolean = True
    is_validator.help_text = "Valide les fiches avant traitement (ex : Chef de Salle)"

    def has_all_access(self, obj):
        return config.group_has_all_access(obj)

    has_all_access.short_description = "Accès complet"
    has_all_access.boolean = True
    has_all_access.help_text = "A accès à toutes les fiches, mêmes celles en traitement par un autre groupe (ex : subdivision QSS)"

    def is_investigator(self, obj):
        return config.group_is_investigator(obj)

    is_investigator.short_description = "Investigateur"
    is_investigator.boolean = True
    is_investigator.help_text = "A accès aux fiches qui lui sont attribuées pour traitement (ex : subdivision hors QSS)"


admin.site.register(SSOConfig, SSOConfigAdmin)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.login_template = "sso/login.html"
