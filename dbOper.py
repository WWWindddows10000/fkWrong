# Database oprator
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! dbOperator version 0.1.0                                        
"""


"""
Database structure:

/settings
- homework.accdb
  - Table: file
    - fid (text, primary key)
    - title (text)
    - subject (num)  1-语文 2-数学 3-英语 4-高考物理 5-竞赛物理 6-化学 7-生物
    - logtime (num, timestamp)
  - Table: paper
    - pid (text, primary key)
    - term (num)
    - type (num)           1-期初 2-第1次月考 3-期中 4-第2次月考 5-期末 6-模拟卷 7-小测
    - subject (num)
    - grade (num) grade字段储存在subid为1的对象中，其他对象为-1
    - subid (num) 1-试卷 2-答题卡 3-答案或其他
  - Table: wrong
    - wid (text, primary key)
    - from (text)
    - sort (text) 题目类型
    - solve (long text) 正解
    - x1 , x2 , y1 , y2 (num) 在引用文件中的截取指导
    - logtime (num, timestamp)
    - info (long text) 如果题目分多页，或有额外补充信息，则填写在info字段
"""

import pyodbc as db
import time
from socketMethods import SocketClient, l
from readSettings import resolveCode

DBPATH = "database\homework.accdb"
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=' + DBPATH + ';'
)
conn = db.connect(conn_str)
cursor = conn.cursor()


class file:
    def __init__(self, fid):
        self.fid = fid
        self.title = None


def exc(order):  # execute an order(if you're too lazy)
    cursor.execute(order)

def searchInsideByISBN(ISBN):
    exc("SELECT inside FROM books WHERE isbn='{}'".format(ISBN))
    reply = cursor.fetchone()
    return reply[0] if reply else 1  # return 1 if not found
def searchByISBN(ISBN):
    exc("SELECT * FROM books WHERE isbn='{}'".format(ISBN))
    reply = cursor.fetchone()
    print(reply)
    if reply is None:
        return 1
    book = Book(reply[0],reply[1],reply[2],reply[3],reply[7])
    return book

def searchByName(name):
    name = name.strip()
    exc("SELECT isbn FROM books WHERE bname LIKE '%{}%' OR sname LIKE '%{}%'".format(name, name))
    reply = cursor.fetchall()
    print(reply)
    if not reply:
        return 1
    if len(reply) == 1:
        return reply[0][0]
    else:
        ans = ''
        for i in reply:
            ans+=(i[0]+'、')
        return ans[:-1]  # remove the last semicolon

def addBook(isbn,bname,sname,sort,term):
    newBook = Book(isbn,bname,sname,sort,term)
    if searchByISBN(isbn) != 1:
        return "Book already exists in the database."
    newBook.prt()
    newBook.addToDB()
    return newBook.bname+' has successfully logged.'  # damn I know register is a better name but I don't want to change it because I am lazy

def deleteBook(isbn):
    exc("DELETE FROM books WHERE isbn='{}'".format(isbn))
    conn.commit()
    print('deleted:{}'.format(isbn))
    return 'deleted:{}'.format(isbn)

def getAllNoBooks():
    exc("SELECT * FROM books WHERE book=False")
    reply = cursor.fetchall()
    if reply == []:
        return 1
    books = ''
    for i in range(len(reply)):
        books += (str(reply[i][0])+'、')
    return books[:-1]

def searchByZone(zone):
    exc("SELECT * FROM books WHERE sort='{}'".format(zone))
    reply = cursor.fetchall()
    if reply == ():
        return 1
    books = []
    for i in range(len(reply)):
        book = Book(reply[i][0],reply[i][1],reply[i][2],reply[i][3],reply[i][7])
        books.append(book)
    return books

def searchByInside(status):
    exc("SELECT * FROM books WHERE inside={}".format(status))
    reply = cursor.fetchall()
    print(reply)
    if reply == []:
        return 1
    books = ''
    for i in range(len(reply)):
        books += (str(reply[i][0])+'、')
    return books[:-1]

def searchByTerm(term):
    exc("SELECT * FROM books WHERE str(validTerm) LIKE '%{}%' OR validTerm=0".format(term))
    reply = cursor.fetchall()
    if reply == []:
        return 1
    books = ''
    for row in reply:
        books += (row[0] + '、')
    return books[:-1]

def searchEzonebooks():
    exc("SELECT * FROM books WHERE sort='E'")
    reply = cursor.fetchall()
    if reply == []:
        return 1
    books = ''
    for i in range(len(reply)):
        books += (str(reply[i][0])+'、')
    return books[:-1]

def getAllBooks(): 
    exc("SELECT * FROM books")
    reply = cursor.fetchall()
    if reply == None:
        return 1
    books = []
    for i in range(len(reply)):
        book = Book(reply[i][0],reply[i][1],reply[i][2],reply[i][3],reply[i][7])
        books.append(book)
    return books

def searchValidBook(thisTerm):
    exc("SELECT * FROM books WHERE validTerm LIKE '%{}%'".format(thisTerm))
    reply = cursor.fetchall()
    if not reply:
        return 1
    books = []
    for row in reply:
        book = Book(row[0], row[1], row[2], row[3], row[7])
        book_dict = {
            'isbn': book.isbn,
            'bname': book.bname,
            'sname': book.sname,
            'sort': book.sort,
            'inside': book.inside(),
            'validterm': (book.validterm == 0) or (thisTerm in str(book.validterm)),
        }
        books.append(book_dict)
    return books



