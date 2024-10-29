# Slack client python package
import slack_sdk

import os

# Creating path
from pathlib import Path

# loading environment variable
from dotenv import load_dotenv

from flask import Flask

from slackeventsapi import SlackEventAdapter



#---------------------------------------------------------------------------------

env_path = Path('.')/ '.env'

load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGING_SECRET'],'/slack/events',app)

client = slack_sdk.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]

# sending message using slack client

@slack_event_adapter.on('message')

def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print(text)
    
    if BOT_ID != user_id:
        client.chat_postMessage(channel='#llm', text=input('Input something'))
    
# here is new comment

if __name__ == "__main__":
    app.run(debug=True)