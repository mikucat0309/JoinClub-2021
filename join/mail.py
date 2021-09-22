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
from subprocess import Popen

def word(name, stID, date, num, is_FCU):
    path = 'Receipt'
    # 校內學生 11010101001
    # 110年份 10101入社費會科 001 第一份
    # 校外學生 11010107001
    # 110年份 10107教材費 001 第一份
    if is_FCU == 'N': # 校外學生
        file1 = os.path.join(path, '黑客社電子收據_社員收執_250.docx')
        file2 = os.path.join(path, '黑客社電子收據_社團存根_250.docx')
        num = "11010107" + str(num).zfill(3)
    else:
        file1 = os.path.join(path, '黑客社電子收據_社員收執.docx')
        file2 = os.path.join(path, '黑客社電子收據_社團存根.docx')
        num = "11010101" + str(num).zfill(3)
    tpl1 = DocxTemplate(file1)
    tpl2 = DocxTemplate(file2)
    context = {
        'name': name,
        'stID': str(stID),
        'date': date,
        'num': num
    }
    if is_FCU == 'N': # 校外學生
        filename = "社費_" + name + stID
    else:
        filename = "社費_" + stID
    pythoncom.CoInitialize() # 加上這行讀取docx時才不會出錯
    path = os.path.join(path, '社費')
    tpl1.render(context)
    tpl1.save(os.path.join(path, filename + '_社員收執.docx'))
    #convert(os.path.join(path, filename + '_社員收執.docx'))
    convert_to_pdf(os.path.join(path, filename + '_社員收執.docx'), path)
    tpl2.render(context)
    tpl2.save(os.path.join(path, filename + '_社團存根.docx'))
    #convert(os.path.join(path, filename + '_社團存根.docx'))
    convert_to_pdf(os.path.join(path, filename + '_社團存根.docx'), path)
    os.remove(os.path.join(path, filename + '_社員收執.docx'))
    os.remove(os.path.join(path, filename + '_社團存根.docx'))

def convert_to_pdf(input_docx, out_folder):
    LIBRE_OFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
    p = Popen([LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
            out_folder, input_docx])
    #print([LIBRE_OFFICE, '--convert-to', 'pdf', input_docx])
    p.communicate()



def mail(name, stID, is_FCU, email):

    context = {
        'name': name,
        'stID': stID,

    }

    subject = "逢甲大學黑客社 - 電子收據 " + context['stID']
    body = "若有任何問題，請聯繫黑客社粉絲專頁！"
    sender_email = "cat891127@gmail.com"
    if is_FCU == 'N':  # 校外學生
        receiver_email = email
    else:
        receiver_email = context['stID'] + "@o365.fcu.edu.tw"
    password = ""  # 信箱密碼

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    path = os.path.join('Receipt', '社費')
    filename = '社費_' + context['stID'] + '_社員收執.pdf'# In same directory as script

      
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
