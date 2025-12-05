# logging methods
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! Logging Methods version 0.1.0                                        
"""

from datetime import datetime as dt
import enum
import logging
import os
from rich.logging import RichHandler

logger = logging.getLogger("all_in_logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/{}.log'.format(dt.now().strftime("%Y%m%H%M")), encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = RichHandler()
console_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logging.getLogger("imapclient").setLevel(logging.WARNING)
logging.getLogger("imaplib").setLevel(logging.WARNING)

class l(enum.Enum):
    """
    I am lazy, I don't want to use 4- or 5-character-long log level.
    So I made this, replacing words into l.(The first letter)
    But this is totally nonsense。 An unnecessary move.
    """
    I = 'INFO'
    W = 'WARN'
    E = 'ERROR'
    F = 'FATAL'
    D = 'DEBUG'

def log(message, level):
    """

    """
    if level == l.I:
        logger.info(message)
    elif level == l.W:
        logger.warning(message)
    elif level == l.E:
        logger.error(message)
    elif level == l.F:
        logger.critical(message)
    elif level == l.D:
        logger.debug(message)
