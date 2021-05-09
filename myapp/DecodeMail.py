from datetime import datetime
from dateutil import parser
class Mail:
  def __init__(self, email,body):
    self.senderName = email['from'].split("<")[0]
    self.email = email['from'].split("<")[1][:-1]
    self.to = email['to']
    self.date = parser.parse(email['date']).strftime('%m-%d-%Y')
    self.subject = email['subject']
    self.body = body

