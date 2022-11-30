from django.db import models

'''
When using many to many fields, SQL queries tend to proliferate when
iterating through a queryset
(because a new query is sent to m2m table for each item).
This can be prevented by prefetching children before iterating
'''


class PrefetchingActionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()\
            .select_related('current_status', 'current_group', 'next_status', 'next_group')


class PrefetchingFormManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .select_related('assigned_to_group', 'status')\
            .prefetch_related('available_actions__next_status', 'assigned_to_group__permissions')
