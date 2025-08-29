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

def exc(order):
    cursor.execute(order)

class File:
    def __init__(self, fid):
        self.fid = fid
        self.title = resolve_code(fid, False)
        self.subject = match_subject(fid)
        self.register_time = time.time()


SQL_SENTENCES = {
    "write_file" : ""
}
