from email.mime.image import MIMEImage
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client


def send_textmessage_alert(alert=""):
    cellphone = 18452422392
    twilio_number = 17068105899
    account = "AC062ffd139b27fde112c817fc516f4400"
    token = "f2e8218c33cd7c37354c9b4cb7892607"

    client = Client(account, token)

    client.messages.create(
        to=cellphone,
        from_=twilio_number,
        body=alert,
        # media_url=["https://demo.twilio.com/owl.png"],
    )


def send_alert(body, subject):
    message = MIMEMultipart()
    message["Subject"] = subject
    # message["From"] = "leldforecast@gmail.com"
    message["From"] = "leldforecast@gmail.com"
    # message["To"] = "dev923757@gmail.com"
    message["To"] = "plaverty@lelwd.com"

    body_content = body
    message.attach(MIMEText(body_content, "html"))

    msgAlternative = MIMEMultipart("alternative")
    message.attach(msgAlternative)

    msg_body = message.as_string()

    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    # server.login(message["From"], "Develop123")
    server.login(message["From"], "@39Ayerrd")
    # server.login(message["From"], "Mwpmatt12")
    server.sendmail(message["From"], message["To"], msg_body)
    server.quit()
