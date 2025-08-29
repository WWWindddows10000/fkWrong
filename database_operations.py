# Database operator
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! dbOperator version 0.1.0                                        
"""

import pyodbc as db
import time
from logging_methods import log, l
from read_settings import resolve_code, match_subject

# Database connection
DBPATH = r"database\db.accdb"
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + DBPATH + ';'
)
try:
    conn = db.connect(conn_str)
    cursor = conn.cursor()
except Exception as e:
    log(f"An error occurred when connecting the database : {e}", l.F)
    log("The program will exit now.", l.F)
    exit(1)
log("Connected to the database.", l.I)


def database_operations(operation, **kwargs):
    """


    """
    match(operation):
        case "i":
            if not kwargs:
                log("Failed to update database : No arguments provided.", l.W)
                return
            table = kwargs["table"]
            columns = []
            placeholders = []
            values = []
            for column, value in kwargs.items():
                columns.append(f'"{column}"')
                placeholders.append('%s')
                values.append(value)
            order = f'INSERT INTO "{table}" ({", ".join(columns)}) VALUES ({", ".join(placeholders)})'
        case "c":
            if not kwargs:
                log("Failed to update database : No arguments provided.", l.W)
                return
            order = f'UPDATE "file" SET "corrected" = 1 WHERE "fid" = "{kwargs["fid"]}"'
        case "r":
            if not kwargs:
                log("Failed to update database : No arguments provided.", l.W)
                return
    try:
        cursor.execute(order)
        db.commit()
    except Exception as e:
        log(f"An error occurred when updating to the database : {e}", l.E)
        db.rollback()


class File:
    def __init__(self, fid):
        self.fid = fid
        self.title = resolve_code(fid, False)
        self.subject = match_subject(fid)
        self.register_time = time.time()


