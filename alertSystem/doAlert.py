from email.mime.image import MIMEImage
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_alert(body):
    message = MIMEMultipart()
    message["Subject"] = "Load Alert"
    # message["From"] = "leldforecast@gmail.com"
    message["From"] = "dev923757@gmail.com"
    message["To"] = "dev923757@gmail.com"

    body_content = body
    message.attach(MIMEText(body_content, "html"))

    msgAlternative = MIMEMultipart("alternative")
    message.attach(msgAlternative)

    msg_body = message.as_string()

    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(message["From"], "Develop123")
    # server.login(message["From"], "@39Ayerrd")
    # server.login(message["From"], "Mwpmatt12")
    server.sendmail(message["From"], message["To"], msg_body)
    server.quit()
