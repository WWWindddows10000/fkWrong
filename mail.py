# 从邮件中收取学校扫描的文件
"""
███████╗██╗  ██╗██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██║ ██╔╝██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ 
█████╗  █████╔╝ ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██╔═██╗ ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║
██║     ██║  ██╗╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝                                                       
fkWrong! MailModule version 0.1.0                                        
"""
import imaplib
import email
import os
from email.header import decode_header
from datetime import datetime

# 文件路径
CREDENTIALS_PATH = "./secret/code.txt"
TEMP_DIR = "./temp/"

# 读取账户和密码
def get_credentials():
    with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        email_address = lines[0].strip()
        password = lines[1].strip()
        return email_address, password

# 建立 IMAP 连接
def connect_imap():
    email_address, password = get_credentials()
    imap = imaplib.IMAP4_SSL("imap.126.com")  # 改成你邮箱对应的 IMAP 服务器
    imap.login(email_address, password)
    return imap

# 获取最近邮件的标题
def get_recent_mails(limit=7):
    imap = connect_imap()
    imap.select("INBOX")
    result, data = imap.search(None, "ALL")
    mail_ids = data[0].split()
    recent_ids = mail_ids[-limit:]

    mails = []
    for i in reversed(recent_ids):
        res, msg_data = imap.fetch(i, "(RFC822)")
        try:
            msg = email.message_from_bytes(msg_data[0][1])
            subject_raw = msg["Subject"]
            if subject_raw is not None:
                subject, _ = decode_header(subject_raw)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
            else:
                subject = ""
            mails.append(subject)
        except (IndexError, TypeError, email.errors.MessageError):
            mails.append("(解析邮件出错)")
    imap.logout()
    return mails

def fetch_pdf_attachment_by_index(index=1):
    imap = connect_imap()
    imap.select("INBOX")
    result, data = imap.search(None, "ALL")
    mail_ids = data[0].split()
    if not mail_ids or index < 1 or index > len(mail_ids):
        imap.logout()
        return None

    # 最新的为1，往前递增
    target_id = mail_ids[-index]
    res, msg_data = imap.fetch(target_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            filename, _ = decode_header(filename)[0]
            if isinstance(filename, bytes):
                filename = filename.decode()
            if filename.lower().endswith(".pdf"):
                os.makedirs(TEMP_DIR, exist_ok=True)
                filepath = os.path.join(TEMP_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                imap.logout()
                return filename
    imap.logout()
    return None
