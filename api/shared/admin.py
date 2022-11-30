from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, path
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django_celery_results.models import GroupResult
import traceback

from .models import config, form
from .safetycube.utils import get_pretty_safetycube_ref, batch_send_to_safetycube
from .tasks import check_graph, clean, refresh_safetycube_for_all


class ExtraButtonsMixin:
    change_list_template = "shared/admin/changelist_with_extra_buttons.html"

    def get_extra_buttons(self):
        # should return action as { title, path, method }
        raise NotImplemented

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [path(extra['path'], extra['method'])
                      for extra in self.get_extra_buttons()]
        return extra_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['extra_buttons'] = self.get_extra_buttons()
        return super().changelist_view(request, extra_context=extra_context)

    def trigger_task(self, request, task, args={}):
        result = task.delay(**args)
        self.message_user(
            request,
            mark_safe("<a href='{}'>Tâche {} ajoutée à la file</a> ({})".format(
                reverse_lazy('admin:django_celery_results_taskresult_changelist'), result.task_id, result.status))
        )
        return HttpResponseRedirect("../")


@admin.register(config.TeamZone)
class TeamZoneAdmin(admin.ModelAdmin):
    model = config.TeamZone
    list_display = ['short_name', 'color']


@admin.register(config.Team)
class TeamAdmin(admin.ModelAdmin):
    model = config.Team
    list_display = ('label', 'zone',)
    search_fields = ('label', 'zone__short_name',)


@admin.register(form.Status)
class StatusAdmin(admin.ModelAdmin):
    model = form.Status
    list_display = ('label', 'is_draft', 'is_waiting', 'is_in_progress',
                    'is_done', 'is_to_be_deleted')


class ActionAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    model = form.AbstractAction
    list_display = ('label', 'is_complete', 'current_status', 'current_group',
                    'next_status', 'next_group', 'rank', 'is_default', 'is_terminal')
    search_fields = ('label', 'current_group__name', 'current_status__label',
                     'next_group__name', 'next_status__label')
    readonly_fields = ["is_complete"]

    def get_extra_buttons(self):
        return [
            {'title': 'Vérifier graph', 'path': 'trigger-check/',
                'method': self.trigger_check}
        ]

    def trigger_check(self, request):
        return self.trigger_task(
            request, check_graph,
            args={'app_label': self.model._meta.app_label,
                  'action_model_name': self.model._meta.model.__name__})


class CounterAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'count')
    search_fields = ['category']


@admin.register(config.Sector)
class SectorAdmin(admin.ModelAdmin):
    model = config.Sector
    list_display = ("label", )
    search_fields = ('label', )


@admin.register(config.SectorGroup)
class SectorGroupAdmin(admin.ModelAdmin):
    model = config.SectorGroup
    list_display = ("label", )
    search_fields = ('label', )


@admin.register(config.Position)
class PositionAdmin(admin.ModelAdmin):
    model = config.Position
    list_display = ("label", )
    search_fields = ('label', )


class FormAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('event_date', 'full_status', 'update_date')
    readonly_fields = ('available_actions', 'uuid')
    actions = ["update_available_actions", 'send_to_safetycube']
    fieldsets = ((None, {
        'fields':
        (('event_date', 'uuid'), ('status', 'assigned_to_group',
                                  'assigned_to_person'), 'available_actions')
    }),)

    def full_status(self, obj):
        if obj.status is not None:
            if obj.assigned_to_group is None:
                return obj.status.label
            if obj.assigned_to_person is not None:
                return "{} {} ({})".format(obj.status, obj.assigned_to_group,
                                           obj.assigned_to_person)
            return "{} {}".format(obj.status, obj.assigned_to_group)
        return "?"

    full_status.short_description = "Etat"

    @admin.action(description="Recalculer les actions possibles")
    def update_available_actions(self, request, queryset):
        for f in queryset.all():
            f.update_available_actions()

    def get_extra_buttons(self):
        buttons = [{
            'title': 'Nettoyer',
            'path': 'trigger-clean/',
            'method': self.trigger_clean
        }]
        if not self.model.options.is_safetycube_enabled():
            buttons += [{
                'title': 'Actualiser SafetyCube',
                'path': 'trigger-refresh/',
                'method': self.trigger_refresh
            }]
        return buttons

    def safetycube_ref(self, obj):
        return get_pretty_safetycube_ref(obj)
    safetycube_ref.short_description = "SafetyCube"

    @admin.action(description="Enregistrer dans SafetyCube")
    def send_to_safetycube(self, request, queryset):
        try:
            if not self.model.options.is_safetycube_enabled():
                self.message_user(
                    request, "Les fonctionnalités SafetyCube ne sont pas disponibles pour ce type de formulaire", level=messages.WARNING)
            else:
                uuid_list = queryset.values_list("uuid", flat=True).all()
                batch_send_to_safetycube(
                    uuid_list, self.model)
        except Exception as e:
            self.message_user(request, e, level=messages.ERROR)
            traceback.print_exc()

    def trigger_clean(self, request):
        return self.trigger_task(request, clean,
                                 args={'app_label': self.model._meta.app_label,
                                       'model_name': self.model._meta.model.__name__})

    def trigger_refresh(self, request):
        if self.model.options.is_safetycube_enabled():
            return self.trigger_task(
                request, refresh_safetycube_for_all,
                args={'app_label': self.model._meta.app_label,
                      'model_name': self.model._meta.model.__name__})
        else:
            self.message_user(
                request, "Les fonctionnalités SafetyCube ne sont pas disponibles pour ce type de formulaire", level=messages.WARNING)


admin.site.unregister(Site)
admin.site.unregister(GroupResult)

try:
    from efneproject.version import __version__
    admin.site.site_header = mark_safe("eFNE Admin <span style='font-size:0.8125rem;'>({})</span>".format(
        __version__))
except:
    admin.site.site_header = "eFNE Admin"
