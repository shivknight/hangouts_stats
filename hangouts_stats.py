#!/usr/bin/python

import json
from pprint import pprint

convo_id = 15

def load_hangouts():
  with open('Hangouts/Hangouts.json') as data_file:
      return json.load(data_file)

def create_user_dict(hangouts):
  users = {}
  participant_data = hangouts["conversation_state"][convo_id]["conversation_state"]["conversation"]["participant_data"]
  for participant in participant_data:
    gaia_id = participant["id"]["gaia_id"]
    name = participant["fallback_name"]
    users[gaia_id] = {"name":name}
  return users

def junk(users):
  count = {}
  events = hangouts["conversation_state"][convo_id]["conversation_state"]["event"]
  #pprint(events)
  for event in events:
    gaia_id = event["sender_id"]["gaia_id"]
    if gaia_id not in count:
      count[gaia_id] = 0
    else:
      count[gaia_id] += 1
#    print users[gaia_id]["name"]
#    print event["chat_message"]["message_content"]["segment"][0]["text"]
#    print ""
  return count

hangouts = load_hangouts()
users = create_user_dict(hangouts)
count = junk(users)
for gaia_id, num in count.iteritems():
  print "{0}: {1}".format(users[gaia_id]["name"], num)
