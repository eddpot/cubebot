"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.MIMEText import MIMEText
import base64
import os
from apiclient import discovery  
from apiclient import errors  

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
store = file.Storage('credentials.json')
creds = store.get()
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Call the Gmail API
def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """

  message = (service.users().messages().send(userId=user_id, body=message).execute())  
  print ('Message Id: %s' %message['id'])  
  return message  




email=create_message('cubebot03@gmail.com','eddpot@gmail.com','Cube Alert!', 'qube')
send_message(service,"me",email)