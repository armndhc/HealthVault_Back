import logging as log

class Logger:
    def __init__(self, log_file='maika_api.log', level=log.INFO):
        log.basicConfig(
            level=level,
            format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %I:%M:%S %p',
            handlers=[
                log.FileHandler(log_file),
                log.StreamHandler()
            ]
        )
        self.logger = log.getLogger()

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        self.logger.critical(message, stacklevel=2)