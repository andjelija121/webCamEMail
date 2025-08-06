import smtplib
from email.message import EmailMessage
from PIL import Image
import io

sender = 'andjelijamdev@gmail.com'
receiver = 'andjelijamdev@gmail.com'
password = "nkfk wcum cjuq yomt"


def send_email(image_path):
        emsg = EmailMessage()

        emsg['Subject'] = 'Someone just appeared at the shop!'
        emsg['From'] = sender
        emsg['To'] = receiver
        emsg.set_content('Here is the picture of the person who just entered your shop.')

        with open(image_path, "rb") as file:
            content = file.read()
        try:
            with Image.open(io.BytesIO(content)) as img:
                subtype = img.format.lower()
        except IOError:
            subtype = None

        emsg.add_attachment(content, maintype="image", subtype=subtype)

        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(sender, password)
        gmail.send_message(emsg)
        gmail.quit()


if __name__ == '__main__':
    send_email('images/10.png')