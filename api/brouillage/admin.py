from django.contrib import admin

from shared.admin import ActionAdmin, CounterAdmin, FormAdmin
from . import models


class RedactorInline(admin.TabularInline):
    model = models.Redactor


class AircraftInline(admin.TabularInline):
    model = models.Aircraft


class SubDataInline(admin.StackedInline):
    model = models.SubData


class BrouillageAdmin(FormAdmin):
    models = models.Brouillage
    list_display = ('event_date', 'full_status', 'frequency', 'update_date')
    inlines = [AircraftInline, RedactorInline, SubDataInline]
    fieldsets = FormAdmin.fieldsets + (('Evènement', {
        'fields': (('frequency', 'cwp'), 'interferences', 'description', 'freq_unusable', 'traffic_impact', 'supp_freq')
    }), )


class PostItInline(admin.TabularInline):
    model = models.PostIt


class BrouillageCounterAdmin(CounterAdmin):
    model = models.BrouillageCounter


class BrouillageActionAdmin(ActionAdmin):
    model = models.BrouillageAction


class InterferenceTypeAdmin(admin.ModelAdmin):
    model = models.InterferenceType
    list_display = ('rank', 'name',)


admin.site.register(models.Brouillage, BrouillageAdmin)
admin.site.register(models.BrouillageAction, BrouillageActionAdmin)
admin.site.register(models.BrouillageCounter, BrouillageCounterAdmin)
admin.site.register(models.InterferenceType, InterferenceTypeAdmin)
