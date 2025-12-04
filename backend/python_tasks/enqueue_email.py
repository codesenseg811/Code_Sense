# python_tasks/enqueue_email.py
if __name__ == "__main__":
    import sys
    from python_tasks.tasks import send_email_task

    if len(sys.argv) < 5:
        print("Usage: enqueue_email.py email subject html admin_email")
        sys.exit(1)

    email = sys.argv[1]
    subject = sys.argv[2]
    html = sys.argv[3]
    admin_email = sys.argv[4]

    send_email_task.delay(email, subject, html, admin_email)
    print(f"Queued email to {email}")
