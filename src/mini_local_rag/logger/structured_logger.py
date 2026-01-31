
import logging
import os
import sys
from typing import Optional

from mini_local_rag.config import Config
from mini_local_rag.logger.log_record import LogRecord


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,):
        super().__init__(fmt, datefmt)

    
    def format(self, record):
        data: LogRecord = getattr(record, 'data')
        return data.model_dump_json(indent=3)

class StructuredLogger:
    __log_file:str ="logs" 
    def __init__(self, config:Config):
        self.logger = logging.getLogger("structured_logger")
        self.logger.setLevel(logging.DEBUG)
        
        # JSON formatter
        formatter = JsonFormatter()

        # File handler (appends to file)
        cwd = os.getcwd()
        log_dir = os.path.join(cwd, config.data_folder)
        log_file_path = os.path.join(log_dir, self.__log_file)
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler (optional)
        if config.show_logs:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, record: LogRecord):
        """Log a message with a specified level and structured fields."""
        extra = {
            'data' :record
        }
        
        self.logger.debug(msg=f"log record for trace_id {record.trace_id}", extra=extra)

