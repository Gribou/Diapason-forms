from shared.model_managers import PrefetchingFormManager


class PrefetchingSimiManager(PrefetchingFormManager):

    def get_queryset(self):
        return super().get_queryset()\
            .select_related('sub_data')\
            .prefetch_related('redactors', 'aircrafts', 'sub_data__postits')
