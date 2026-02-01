
import logging
import os
import sys
from typing import Optional

from mini_local_rag.config import Config
from mini_local_rag.logger.log_record import LogRecord


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None,):
        """
        Initialize the JSON formatter.

        Args:
            fmt (Optional[str]): Format for the log message (not used for JSON output).
            datefmt (Optional[str]): Format for the date and time (not used for JSON output).
        """
        super().__init__(fmt, datefmt)

    
    def format(self, record):
        """
        Format the log record as JSON.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The log record formatted as a JSON string.
        """
        data: LogRecord = getattr(record, 'data')
        return data.model_dump_json(indent=3)

class StructuredLogger:
    """Logger that outputs structured logs to both file and console, with JSON format."""

    __log_file:str ="logs" 
    def __init__(self, config:Config):
        """
        Initialize the StructuredLogger.

        Args:
            config (Config): Configuration object containing settings for logging.
        """
        self.logger = logging.getLogger("structured_logger")
        self.logger.setLevel(logging.DEBUG)
        self.config=config

        
        # JSON formatter
        formatter = JsonFormatter()

        #log t file
        # File handler (appends to file)
        cwd = os.getcwd()
        log_dir = os.path.join(cwd, config.data_folder)
        log_file_path = os.path.join(log_dir, self.__log_file)
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


        # log to console
        self.console_logger = logging.getLogger("structured_logger_console")
        self.console_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.console_logger.addHandler(console_handler)


    def log(self, record: LogRecord):
        """
        Log a message with a specified level and structured fields.

        Args:
            record (LogRecord): The log record containing data to be logged.
        """
        extra = {
            'data' :record
        }
        if (self.config.show_logs):
            self.console_logger.debug(msg=f"log record for trace_id {record.trace_id}", extra=extra)

        self.logger.debug(msg=f"log record for trace_id {record.trace_id}", extra=extra)

