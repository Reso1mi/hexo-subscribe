from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import smtplib
from config import Config


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(to_addrs, subject, text, msg_type):
    from_addr = Config.account
    password = Config.password
    smtp_server = Config.smtp_server
    port = Config.smtp_port
    msg = MIMEText(text, msg_type, "utf-8")
    msg["From"] = _format_addr("%s <%s>" % ("Tadow", from_addr))
    # msg["To"] = Header(",".join(to_addrs), "utf-8")
    msg["Subject"] = Header(subject, "utf-8").encode()
    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()
