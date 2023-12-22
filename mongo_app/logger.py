import logging
from django.conf import settings

logging.config.dictConfig(settings.LOGGING)


class Logging:
    def __init__(self,name):
        self.logger = logging.getLogger(name)

    def info_msg(self, message):
        self.logger.info(message)

    def error_msg(self, message):
        self.logger.error(message)
