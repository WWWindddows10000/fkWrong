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
import os
from datetime import datetime
from imapclient import IMAPClient
from email.header import decode_header
import email


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
# 建立 IMAPClient 连接
def connect_imap():
    email_address, password = get_credentials()
    server = IMAPClient("imap.126.com", ssl=True)
    server.login(email_address, password)
    return server


def get_recent_mails(limit=7):
    email_address, password = get_credentials()
    dates = []

    try:
        with IMAPClient("imap.126.com", ssl=True, timeout=10) as server:
            server.id_({"name": "fkWrongFetcher", "version": "1.0"})
            server.login(email_address, password)
            server.select_folder("INBOX", readonly=True)

            messages = server.search(["ALL"])
            if not messages:
                return ["(没有找到邮件)"]

            recent_ids = messages[-limit:]
            fetch_data = server.fetch(recent_ids, ["ENVELOPE"])

            for msgid in reversed(recent_ids):
                try:
                    envelope = fetch_data[msgid][b"ENVELOPE"]
                    date_obj = envelope.date

                    # 安全格式化日期
                    if date_obj and isinstance(date_obj, datetime):
                        dates.append(date_obj.strftime("%Y-%m-%d(%a) %H:%M:%S"))
                    else:
                        dates.append("(无时间信息)")
                except Exception as e:
                    dates.append(f"(解析失败: {e})")

    except Exception as e:
        dates.append(f"(连接失败: {e})")

    return dates


# 下载指定邮件编号中的 PDF 附件
def fetch_pdf_attachment_by_index(index=1):
    server = connect_imap()
    server.id_({"name": "IMAPClient", "version": "2.1.0"})
    server.select_folder("INBOX", readonly=False)
    messages = server.search("ALL")

    if not messages or index < 1 or index > len(messages):
        server.logout()
        return None

    target_id = messages[-index]
    msg_data = server.fetch(target_id, ["RFC822"])
    raw_msg = msg_data[target_id][b"RFC822"]
    msg = email.message_from_bytes(raw_msg)

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if filename:
            filename, _ = decode_header(filename)[0]
            if isinstance(filename, bytes):
                filename = filename.decode(errors="ignore")
            if filename.lower().endswith(".pdf"):
                os.makedirs(TEMP_DIR, exist_ok=True)
                filepath = os.path.join(TEMP_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                server.logout()
                return filename
    server.logout()
    return None