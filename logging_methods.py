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
from rich.logging import RichHandler

logger = logging.getLogger("all_in_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/{}.log'.format(dt.now().strftime("%Y%m%H%M%S%f")), encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = RichHandler()
console_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logging.getLogger("imapclient").setLevel(logging.WARNING)
logging.getLogger("imaplib").setLevel(logging.WARNING)

class l(enum.Enum):
    I = 'INFO'
    W = 'WARN'
    E = 'ERROR'
    F = 'FATAL'
    D = 'DEBUG'

def log(message, level):
    """

    """
    match level:
        case l.I:
            logger.info(message)
        case l.W:
            logger.warning(message)
        case l.E:
            logger.error(message)
        case l.F:
            logger.critical(message)
        case l.D:
            logger.debug(message)
