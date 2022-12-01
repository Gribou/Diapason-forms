from django.contrib import admin


from shared.admin import ActionAdmin, FormAdmin, CounterAdmin
from . import models


class RedactorInline(admin.TabularInline):
    model = models.Redactor


class AircraftInline(admin.TabularInline):
    model = models.Aircraft


class CdsReportInline(admin.StackedInline):
    model = models.CdsReport


class AttachmentInline(admin.TabularInline):
    model = models.Attachment


class SubDataInline(admin.StackedInline):
    model = models.SubData


class TCASReportInline(admin.StackedInline):
    model = models.TCASReport


class FneAdmin(FormAdmin):
    model = models.Fne
    list_display = ('event_date', 'full_status', 'zones', 'aircraft_list',
                    'has_tcas', 'safetycube_ref', 'update_date')
    inlines = [
        AircraftInline, RedactorInline, CdsReportInline, TCASReportInline,
        AttachmentInline, SubDataInline
    ]
    readonly_fields = FormAdmin.readonly_fields + \
        ('has_tcas', 'aircraft_list',)
    fieldsets = FormAdmin.fieldsets + (('Evènement', {
        'fields':
        (('secteur', 'position', 'regroupement'), ('lieu', 'isp', 'has_tcas'),
         'event_types', 'description', 'drawing')
    }), ('Evènement technique', {
        'fields': (('tech_event', 'tech_actions_done'))
    }),)

    def has_tcas(self, obj):
        return obj.tcas_report is not None

    has_tcas.boolean = True
    has_tcas.short_description = "Rapport TCAS"

    def aircraft_list(self, obj):
        return ', '.join([a.callsign for a in obj.aircrafts.all()])

    aircraft_list.short_description = "Aéronefs concernés"


class PostItInline(admin.TabularInline):
    model = models.PostIt


class EventTypeAdmin(admin.ModelAdmin):
    model = models.EventType
    list_display = ('rank', 'name', 'is_tcas')


class TechActionAdmin(admin.ModelAdmin):
    model = models.TechAction
    list_display = ('pk', 'name', 'helperText')


class TechEventTypeAdmin(admin.ModelAdmin):
    model = models.TechEventType
    list_display = ('rank', 'name', 'helperText')
    filter_horizontal = ('actions',)


class FneCounterAdmin(CounterAdmin):
    model = models.FneCounter


class RoleAdmin(admin.ModelAdmin):
    model = models.Role
    list_display = ('label', 'rank', )


class FneActionAdmin(ActionAdmin):
    model = models.FneAction


admin.site.register(models.Fne, FneAdmin)
admin.site.register(models.FneAction, FneActionAdmin)
admin.site.register(models.EventType, EventTypeAdmin)
admin.site.register(models.TechEventType, TechEventTypeAdmin)
admin.site.register(models.TechAction, TechActionAdmin)
admin.site.register(models.FneCounter, FneCounterAdmin)
admin.site.register(models.Role, RoleAdmin)
