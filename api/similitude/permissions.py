from constance import config
from shared.permissions import FeatureActivated


class SimiActivated(FeatureActivated):

    def is_feature_activated(self):
        return config.SHOW_SIMI
