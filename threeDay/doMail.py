from email.mime.image import MIMEImage
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(body):
    message = MIMEMultipart()
    message["Subject"] = "Three Day Forecast"
    # message["From"] = "leldforecast@gmail.com"
    message["From"] = "dev923757@gmail.com"
    # message["To"] = "peakalert@lelwd.com"
    message["To"] = "dev923757@gmail.com"

    body_content = body
    message.attach(MIMEText(body_content, "html"))

    msgAlternative = MIMEMultipart("alternative")
    message.attach(msgAlternative)

    with open("figure.png", "rb") as fp:
        msgImage = MIMEImage(fp.read())
    msgImage.add_header("Content-ID", "<image1>")
    message.attach(msgImage)

    with open("figure2.png", "rb") as fp2:
        msgImage2 = MIMEImage(fp2.read())
    msgImage2.add_header("Content-ID", "<image2>")
    message.attach(msgImage2)

    with open("figure3.png", "rb") as fp3:
        msgImage3 = MIMEImage(fp3.read())
    msgImage3.add_header("Content-ID", "<image3>")
    message.attach(msgImage3)

    msg_body = message.as_string()

    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(message["From"], "huggzpnmqpntvtbf")
    # server.login(message["From"], "@39Ayerrd")

    server.sendmail(message["From"], message["To"], msg_body)
    server.quit()
