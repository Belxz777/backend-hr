# logging_handler.py
import logging
from collections import deque

class EndpointLogHandler(logging.Handler):
    def __init__(self, max_len=1000):
        super().__init__()
        self.logs = deque(maxlen=max_len)
    
    def emit(self, record):
        self.logs.append({
            'level': record.levelname,
            'message': self.format(record),
            'timestamp': record.created,
            'module': record.module
        })

# Глобальный обработчик
endpoint_handler = EndpointLogHandler()