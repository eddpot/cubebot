#import twitter credentials
from credentials import *

#import tweepy module for interacting with twitter api
import tweepy

#import gmail stuff
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.MIMEText import MIMEText
import base64
import os
from apiclient import discovery  
from apiclient import errors  
   
   

# Setup the Gmail API
# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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
  try:  
      message = (service.users().messages().send(userId=user_id, body=message).execute())  
      print ('Message Id: %s' %message['id'])  
      return message  
  except errors.HttpError, error:  
      print ('An error occurred: %s' % error)  



#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if ('cube' in status.text.lower()):
        	print(status.user.name)
        	api.update_status(status.user.name + ' said Cube! >>>> https://twitter.com/magiconline/status/'+str(status.id))
        	email=create_message('cubebot03@gmail.com','eddpot@gmail.com','Cube Alert!',status.user.name + ' said Cube! View the Tweet here https://twitter.com/mashimiii/status/'+str(status.id))
        	send_message(service,"me",email)
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print ('420')
            return False

        # returning non-False reconnects the stream, with backoff.



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=['900694717'])



