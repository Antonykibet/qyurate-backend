import smtplib
import ssl
from email.message import EmailMessage
from django.conf import settings

import logging

LOGGER = logging.getLogger(__name__)


SMTP_SERVER = settings.SMTP_SERVER
PORT = settings.SMTP_PORT
SENDER_EMAIL = settings.ADMIN_EMAIL
APP_PASSWORD = settings.APP_PASSWORD

def send_email(subject, body, to, html=False, html_body=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to
    try:
        # Send the email
        context = ssl.create_default_context()
        if html:
            msg.add_alternative(html_body, subtype='html')
        with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
    except Exception:
        LOGGER.error('Failed to send email', exc_info=True)