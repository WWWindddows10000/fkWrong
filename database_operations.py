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

import time
import pyodbc as db
from traits.trait_types import false

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
    General database operations
    :param operation: [i]nsert, [c]orrect, [r]emove, [s]earch, [e]xist
    :param kwargs: table, key-value pairs, fid
    """
    if not kwargs:
        log("Failed to update database : No arguments provided.", l.W)
        return False
    if operation == "e":
        return True if database_operations('s',**kwargs) != [] else False
    elif operation == "i" or operation == "r" or operation == "s":
        table = kwargs["table"]
        where_clauses = []   # For the remove operation
        values = []
        conditions = kwargs.copy()
        conditions.pop('table')
        for column, value in conditions.items():
            where_clauses.append(f'"{column}" = ?')  # Used a placeholder to avoid SQL injection
            values.append(value)
        if operation == "i":
            if database_operations('s', table=table, fid=kwargs['fid']) != []:
                log("Record already exists.", l.W)
                return False
            columns = list(conditions.keys())
            placeholders = ['?'] * len(columns)
            order = f'INSERT INTO "{table}" ({", ".join(f'"{c}"' for c in columns)}) VALUES ({", ".join(placeholders)})'
        else:
            if not where_clauses:
                log("Failed to delete or search from database: No WHERE conditions provided.", l.W)
                return False
            where_clause_str = " AND ".join(where_clauses)
            if operation == "r":
                if database_operations('s', **kwargs) == []:
                    log("There are no records to delete.", l.W)
                    return False
                order = f'DELETE FROM "{table}" WHERE {where_clause_str}'
            else:
                order = f'SELECT * FROM "{table}" WHERE {where_clause_str}'
        values = tuple(values)
    elif operation == "c":
        values = (kwargs['fid'],)
        order = f'UPDATE "file" SET "corrected" = 1 WHERE "fid" = ?'
    else:
        log(f"database_operations() got an unexpected keyword argument 'operation' : {operation}", l.W)
        return False
    try:
        cursor.execute(order, values)
        if operation != "s":
            conn.commit()
        else:
            return cursor.fetchall()
    except Exception as exception:
        log(f"An error occurred when updating to the database : {exception} \n order : {order}\nvalues : {values}", l.E)
        conn.rollback()
        if operation == "s":
            return []
    log(f"Database operation \n '{order}' \n is successfully executed with values \n {values}.", l.I)
    return True


class File:
    """
    A single file
    :param fid: The ID of the file + page
    :ivar in_the_database: True if the file is in the database
    """
    in_the_database = False
    def __init__(self, fid):
        self.fid = fid
        in_the_database = database_operations('e', table='file', fid=fid)
        if not in_the_database:
            self.title = resolve_code(fid, False)
            self.subject = match_subject(fid)
            self.register_time = time.time()
            self.corrected = False
        else:
            record = database_operations('s', table='file', fid=fid)[0][1:]
            self.title, self.subject, self.register_time, self.corrected = record


