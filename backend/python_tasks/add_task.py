import sys
from tasks import send_email_task

email = sys.argv[1]
subject = sys.argv[2]
html = sys.argv[3]
admin_email = sys.argv[4]

send_email_task.delay(email, subject, html, admin_email)
print(f"Queued email to {email}")
