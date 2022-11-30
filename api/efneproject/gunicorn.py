import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)
        self.access_log.addFilter(HealthCheckFilter())


class HealthCheckFilter(logging.Filter):
    # do not log healthcheck url access
    def filter(self, record):
        return record.getMessage().find("/api/health/") == -1
