from dataclasses import dataclass
from enum import Enum
import datetime
import os
from typing import Optional
from colorama import Fore, Style, init

class LogLevel(Enum):
    INFO = ("INFO", Fore.WHITE)
    ERROR = ("ERROR", Fore.RED)
    STATUS = ("STATUS", Fore.GREEN)

@dataclass
class LogConfig:
    LOG_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    LATEST_LOG: str = 'latest.log'
    TIME_FORMAT: str = "%H:%M:%S"
    FILE_TIME_FORMAT: str = "%d-%m-%Y_%H-%M-%S.log"

class Logger:
    def __init__(self):
        init()
        self.config = LogConfig()
        self._ensure_log_directory()
        
    def _ensure_log_directory(self) -> None:
        if not os.path.exists(self.config.LOG_DIR):
            os.makedirs(self.config.LOG_DIR)
            
    @property
    def latest_log_path(self) -> str:
        return os.path.join(self.config.LOG_DIR, self.config.LATEST_LOG)

    def _log(self, message: str, level: LogLevel) -> None:
        current_time = datetime.datetime.now().strftime(self.config.TIME_FORMAT)
        console_message = f"{level.value[1]}[{current_time} {level.value[0]}]{Style.RESET_ALL} {message}"
        file_message = f"{current_time} {level.value[0]}: {message}"
        
        print(console_message)
        with open(self.latest_log_path, 'a', encoding='utf-8') as f:
            f.write(file_message + "\n")

    def info(self, message: str) -> None:
        self._log(message, LogLevel.INFO)

    def error(self, message: str) -> None:
        self._log(message, LogLevel.ERROR)

    def status(self, message: str) -> None:
        self._log(message, LogLevel.STATUS)

    def rotate_log_file(self) -> None:
        if os.path.exists(self.latest_log_path):
            creation_time = os.path.getctime(self.latest_log_path)
            new_filename = datetime.datetime.fromtimestamp(creation_time).strftime(
                self.config.FILE_TIME_FORMAT
            )
            new_path = os.path.join(self.config.LOG_DIR, new_filename)
            os.rename(self.latest_log_path, new_path)
            self.info(f"Log rotated to {new_filename}")
