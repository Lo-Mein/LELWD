from email.mime.image import MIMEImage
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def send_mail(body):
    message = MIMEMultipart()
    message['Subject'] = 'Three Day Forecast'
    message['From'] = 'dev923757@gmail.com'
    message['To'] = 'dev923757@gmail.com'

    body_content = body
    message.attach(MIMEText(body_content, "html"))

    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)

    fp = open('figure.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], 'Develop123')
    server.sendmail(message['From'], message['To'], msg_body)
    server.quit()