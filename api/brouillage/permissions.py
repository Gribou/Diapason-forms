from constance import config

from shared.permissions import FeatureActivated


class BrouillageActivated(FeatureActivated):

    def is_feature_activated(self):
        return config.SHOW_BROUILLAGE
