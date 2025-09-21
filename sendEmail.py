import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def sendMail(mail_content, receiver_address, docPath):
    sender_address = "msohaibajcl@gmail.com"
    sender_pass = "jmromdtlecqztqzl"  # Use 16-char app password, not Gmail password

    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    message["Subject"] = "APPROVAL SYSTEM UPDATES"

    # Body
    message.attach(MIMEText(mail_content, "html"))

    # Attachments
    for f in docPath:
        file_name = os.path.basename(f)
        with open(f, "rb") as attach_file:
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attach_file.read())
            encoders.encode_base64(payload)
            payload.add_header("Content-Disposition", "attachment", filename=file_name)
            message.attach(payload)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as session:
        session.login(sender_address, sender_pass)
        session.sendmail(sender_address, receiver_address, message.as_string())

    print("Mail Sent")
