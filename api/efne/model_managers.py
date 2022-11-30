from shared.model_managers import PrefetchingFormManager


class PrefetchingFneManager(PrefetchingFormManager):

    def get_queryset(self):
        return super().get_queryset()\
            .select_related('tcas_report', 'cds_report', 'sub_data')\
            .prefetch_related(
                'event_types', 'redactors__team__zone', 'aircrafts',
                'tech_event__actions', 'tech_actions_done', 'attachments', 'sub_data__postits'
        )
