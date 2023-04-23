
import smtplib
from email.mime.text import MIMEText
from base64 import b64encode, b64decode

def send_email(subject, body, sender, recipients, password):
    """
    Email module for sending registration
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

def compute_email(email, uuid, db_id):
    subject = "Verification email"
    encoded_db_id = str(b64encode(str(db_id).encode('ascii')).decode())
    body = "Please verify your email for using acshealth (this is not phishing, trust us):\
          http://localhost:5000/register/{}"
    body = body.format(encoded_db_id + "ñ" + str(uuid))
    sender = "official.acshealth@gmail.com"
    recipients = [email]
    # TODO: get this from env
    password = "kjgctwqjifqovwyk"
    send_email(subject, body, sender, recipients, password)
