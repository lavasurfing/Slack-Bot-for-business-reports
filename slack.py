# Slack client python package
import importlib.util
import slack_sdk

import os,sys


# Creating path
from pathlib import Path

# loading environment variable
from dotenv import load_dotenv

from flask import Flask, request, Response

from slackeventsapi import SlackEventAdapter

# importing module

# Add the path to the components directory
sys.path.insert(0,'C:/Users/Ashish/Documents/GitHub Repos/smart-chat-2/Universal-Dataset-Chatbot-with-LLM')

# Import the function from r.py
from response import get_final_response

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
    
    # sample query
    q1 = 'Plot an bar chart of month-wise total Quantity for each gender  and Product Category for the year 2023 based on the Date column'
    
    file_link = get_final_response(q1)
    
    if BOT_ID != user_id:
        # client.chat_postMessage(channel='#llm', text=input('Input something'))
            response = client.files_upload_v2(
            channel="C07T5JJHYUT",
            file=file_link,
            title="OK",
            initial_comment="here is your pic",
            filetype="auto"  # Optional: can specify file type like "png", "jpg" if known
        )
            print(response)
    
# Slash Command
@app.route('/send-mark-text', methods=['POST'])
def send_text():
    data = request.form
    

if __name__ == "__main__":
    app.run(debug=True)