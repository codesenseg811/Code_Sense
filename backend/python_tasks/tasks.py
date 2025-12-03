from celery import Celery
from email.mime.text import MIMEText
import smtplib
import ssl
import os
import logging

from dotenv import load_dotenv
load_dotenv()


app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

logger = logging.getLogger(__name__)

# Load env variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))   # 587 = STARTTLS, 465 = SSL
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Admin")
USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() in ("true", "1", "yes")


def send_real_email(to_email, subject, html, reply_to=None):
    if not SMTP_HOST:
        raise RuntimeError("SMTP_HOST is not set")

    if not SMTP_USER or not SMTP_PASS:
        raise RuntimeError("SMTP_USER/SMTP_PASS missing in environment")

    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
    msg["To"] = to_email

    if reply_to:
        msg["Reply-To"] = reply_to

    context = ssl.create_default_context()

    # ---------- SSL MODE (port 465) ----------
    if USE_SSL or SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=25) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
            logger.info(f"Email sent (SSL) to {to_email}")
        return

    # ---------- STARTTLS MODE (port 587) ----------
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25) as server:
        server.ehlo()  # identify
        server.starttls(context=context)  # upgrade connection
        server.ehlo()  # re-identify after TLS
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
        logger.info(f"Email sent (STARTTLS) to {to_email}")


@app.task(bind=True)
def send_email_task(self, to_email, subject, html, admin_email):
    print(f"Sending to {to_email}...")

    try:
        send_real_email(
            to_email=to_email,
            subject=subject,
            html=html,
            reply_to=admin_email
        )
        print("Sent!")
    except Exception as e:
        print(f"Email failed: {e}")
        raise self.retry(exc=e, countdown=5)
