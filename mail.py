from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
import smtplib
import config


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(to_addrs, subject, text, msg_type):
    client_cfg = config.CLIENT_CONFIG
    from_addr = client_cfg['account']
    password = client_cfg['password']
    smtp_server = client_cfg['smtp_server']
    port = client_cfg['smtp_port']
    msg = MIMEText(text, msg_type, "utf-8")
    msg["From"] = _format_addr("%s <%s>" % ("Tadow", from_addr))
    # msg["To"] = Header(",".join(to_addrs), "utf-8")
    msg["Subject"] = Header(subject, "utf-8").encode()
    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()
