from __future__ import print_function
import os.path
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails(service):
	result = service.users().messages().list(userId='me').execute()

	# We can also pass maxResults to get any number of emails. Like this:
	# result = service.users().messages().list(maxResults=200, userId='me').execute()
	messages = result.get('messages')

	# messages is a list of dictionaries where each dictionary contains a message id.

	# iterate through all the messages
	for msg in messages:
		# Get the message from its id
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()

		# Use try-except to avoid any Errors
		try:
			# Get value of 'payload' from dictionary 'txt'
			payload = txt['payload']
			headers = payload['headers']

			# Look for Subject and Sender Email in the headers
			for d in headers:
				if d['name'] == 'Subject':
					subject = d['value']
				if d['name'] == 'From':
					sender = d['value']

			# The Body of the message is in Encrypted format. So, we have to decode it.
			# Get the data and decode it with base 64 decoder.
			parts = payload.get('parts')[0]
			data = parts['body']['data']
			data = data.replace("-","+").replace("_","/")
			decoded_data = base64.b64decode(data)

			# Now, the data obtained is in lxml. So, we will parse
			# it with BeautifulSoup library
			#soup = BeautifulSoup(decoded_data , "lxml")
			#body = soup.body()

			# Printing the subject, sender's email and message
			print("Subject: ", subject)
			print("From: ", sender)
			print("Message: ",decoded_data )
			print('\n')
		except:
			pass


def show_chatty_threads(service, user_id='me'):
    threads = service.users().threads().list(userId=user_id).execute().get('threads', [])
    for thread in threads:
        tdata = service.users().threads().get(userId=user_id, id=thread['id']).execute()
        nmsgs = len(tdata['messages'])

        if nmsgs > 2:    # skip if <3 msgs in thread
            msg = tdata['messages'][0]['payload']
            subject = ''
            for header in msg['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            if subject:  # skip if no Subject line
                print('- %s (%d msgs)' % (subject, nmsgs))

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=5050)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    getEmails(service)
    #show_chatty_threads(service, user_id='me')
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


if __name__ == '__main__':
    main()