import logging
import logging.handlers
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'time': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'name': record.name,
        }
        if hasattr(record, 'exc_info') and record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

class AdvancedLogger:
    def __init__(self, name, log_file, max_bytes=10*1024*1024, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(JSONFormatter())

        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(self.mask_api_keys(msg))

    def info(self, msg):
        self.logger.info(self.mask_api_keys(msg))

    def warning(self, msg):
        self.logger.warning(self.mask_api_keys(msg))

    def error(self, msg):
        self.logger.error(self.mask_api_keys(msg))

    @staticmethod
    def mask_api_keys(msg):
        # Пример маскировки API ключей
        # Здесь следует добавить логику маскировки реальных API ключей
        return msg.replace('API_KEY', '****')  # Замена API_KEY на ****

# Пример использования
# logger = AdvancedLogger(name='my_logger', log_file='my_log.json')
# logger.info('This is an info message with API_KEY')
