import smtplib
import time
import imaplib
import email
import os
import traceback 
from myapp.DecodeMail import Mail
from .models import User
from email.message import EmailMessage


#
# ORG_EMAIL = "@gmail.com"
# FROM_EMAIL = "voicemail015" + ORG_EMAIL
# FROM_PWD = "hesigoasbpvvtrkf"
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993
ALL = "ALL"
SEEN = 'SEEN'
UNSEEN = 'UNSEEN'
INBOX = 'INBOX'
SPAM = 'SPAM'
SENT = '"[Gmail]/Sent Mail"'
STARRED = 'STARRED'
def ReadMails(id, gpass):
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(id, gpass)
        mail.select(INBOX)

        data = mail.search(None, ALL)
        print(data)
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        MailList = []
        for i in range(latest_email_id,first_email_id, -1)[:20]:
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    auth_results = msg.get("Authentication-Results", None)
                    content_type = msg.get_content_type()
                    body = msg.get_payload()

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                m = Mail(msg,body)   
                                MailList.append(m)            
                    if(content_type == "text/plain"):
                        m = Mail(msg,body)   
                        MailList.append(m)
        for m in MailList:
            print("From: "+m.email)
            # print("To: "+m.to)
            # print("Date: "+m.date)
            print("subject: "+m.subject)  
            # print("body: "+m.body)
        return MailList
    except Exception as e:
        traceback.print_exc() 
        print(str(e))


def sendMail(userid,gpass,receiverMail,sub,message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = sub
    msg['From'] = userid
    msg['To'] = receiverMail

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(userid, gpass)
    server.send_message(msg)
    server.quit()