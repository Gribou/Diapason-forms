from shared.model_managers import PrefetchingFormManager
'''
When using many to many fields, SQL queries tend to proliferate when
iterating through a queryset
(because a new query is sent to m2m table for each item).
This can be prevented by prefetching children before iterating
'''


class PrefetchingBrouillageManager(PrefetchingFormManager):

    def get_queryset(self):
        return super().get_queryset()\
            .select_related('sub_data')\
            .prefetch_related('redactors', 'aircrafts', 'sub_data__postits',
                              'redactors__team__zone')
