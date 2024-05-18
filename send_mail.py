from config import config
import smtplib
from email.message import EmailMessage

def send_mail(email_content, email, subject):
    localhost = config['recovery']['localhost']
    host = config['recovery']['host']
    port = config['recovery']['port']
    sender_login = config['recovery']['login']
    sender_password = config['recovery']['password']
    sender = config['recovery']['sender']

    server = smtplib.SMTP_SSL(host, port,  local_hostname=localhost, timeout=120)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email
    msg.set_content(email_content, subtype='html')

    server.login(str(sender_login), str(sender_password))
	
    resp = {'status': False, 'error': ''}
    try:
        resp['status'] = True
        server.sendmail(sender, [email], msg.as_string())
    except:
        resp['status'] = False
        resp['error'] = 'Неверный адрес почты'
    finally:
        server.quit()
        return resp

