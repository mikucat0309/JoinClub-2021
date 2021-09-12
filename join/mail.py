from docxtpl import DocxTemplate
from docx2pdf import convert
import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pythoncom

def word(name,stID,data,num):
    path = 'Receipt'
    file = os.path.join(path, '黑客社電子收據.docx')
    tpl = DocxTemplate(file)
    
    context = {
        'name': name,
        'stID': str(stID),
        'date': data,
        'num': num
    }
    pythoncom.CoInitialize() # 加上這行讀取docx時才不會出錯
    tpl.render(context)
    tpl.save(os.path.join(path, context['stID'] + '.docx'))
    convert(os.path.join(path, context['stID'] + '.docx'))


def mail(name, stID):
    context = {
        'name': name,
        'stID': stID,
        'date': 'yyyymmdd',
        'num': '0001'
    }

    subject = "逢甲大學黑客社 - 電子收據 " + context['stID']
    body = "若有任何問題，請聯繫黑客社粉絲專頁！"
    sender_email = "cat891127@gmail.com"
    receiver_email = context['stID'] + "@o365.fcu.edu.tw"
    password = "891127cat"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    path = 'Receipt'
    filename = context['stID'] + '.pdf'# In same directory as script

      
    # Open PDF file in binary mode
    with open(os.path.join(path, filename), "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
