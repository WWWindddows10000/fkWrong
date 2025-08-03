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

import enum
import logging
from rich.logging import RichHandler
from datetime import datetime as dt

file_handler = logging.FileHandler('logs/{}.log'.format(dt.now().strftime("%Y%m%H%M%S%f")), encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

class l(enum.Enum):
    I = 'INFO'
    W = 'WARN'
    E = 'ERROR'
    F = 'FATAL'
    D = 'DEBUG'

def log(message, type):
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger("rich")
    logger.addHandler(file_handler)
    match type:
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