import smtplib
import email


def send_email(sender, recipient, subject, body, send=True):
    message = email.mime.text.MIMEText(body)

    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    if send:
        s = smtplib.SMTP()
        s.connect()
        s.sendmail(sender, [recipient], message.as_string())
        s.close()

    return message

