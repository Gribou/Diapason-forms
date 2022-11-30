from django.contrib import admin

from shared.admin import ActionAdmin, CounterAdmin, FormAdmin
from . import models

class RedactorInline(admin.TabularInline):
    model = models.Redactor


class AircraftInline(admin.TabularInline):
    model = models.Aircraft


class SubDataInline(admin.StackedInline):
    model = models.SubData


class SimiAdmin(FormAdmin):
    models = models.Simi
    list_display = ('event_date', 'full_status',
                    'aircraft_list', 'safetycube_ref', 'update_date')
    inlines = [AircraftInline, RedactorInline, SubDataInline]
    readonly_fields = FormAdmin.readonly_fields + ('aircraft_list',)
    fieldsets = FormAdmin.fieldsets + (('Evènement', {
        'fields': (('with_incident',), ('description',))
    }),)

    def aircraft_list(self, obj):
        return ', '.join([a.callsign for a in obj.aircrafts.all()])

    aircraft_list.short_description = "Aéronefs concernés"


class PostItInline(admin.TabularInline):
    model = models.PostIt


class SimiCounterAdmin(CounterAdmin):
    model = models.SimiCounter


class SimiActionAdmin(ActionAdmin):
    model = models.SimiAction


admin.site.register(models.Simi, SimiAdmin)
admin.site.register(models.SimiAction, SimiActionAdmin)
admin.site.register(models.SimiCounter, SimiCounterAdmin)
