import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('All is Good, Everything is working fine')

msg['Subject'] = 'This is test message'
msg['From'] = "sender8@gmail.com"
msg['To'] = "recievers@gmail.com"

# Send the message via our own SMTP server.
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("sender@gmail.com", "password")
server.send_message(msg)
server.quit()