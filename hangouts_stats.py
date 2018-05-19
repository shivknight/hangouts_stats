#!/usr/bin/python
import sys

import json
import pprint
import argparse

class User:

  gaia_id = None
  def __init__(self, gaia_id):
    self.gaia_id =  gaia_id
    return

class Conversation:
  conversation_id = None
  users = set()

  def __init__(self, conversation_json):
    self.conversation_id = conversation_json["conversation_state"]["conversation_id"]["id"]
    return

  def __str__():
    return conversation_id

class Hangouts:
  hangouts_json = {}
  user_dict = {}
  conversations = set()

  def __init__(self, filepath):

    # Load hangouts json
    with open(filepath) as data_file:
      self.hangouts_json = json.load(data_file)

    self.conversations = buildConversations()

    return

  def buildConversations(hangouts):
    _convos = set()

    for c in hangouts["conversation_state"]:
      _convos.add(Conversation(c))

    return _convos

  def create_user_dict(hangouts, conversation_index):
    gaia_ids = {}
    fallback_names = {}
    participant_data = hangouts["conversation_state"][conversation_index]["conversation_state"]["conversation"]["participant_data"]
    for participant in participant_data:
      gaia_id = participant["id"]["gaia_id"]
      name = participant.get("fallback_name",participant["id"]["gaia_id"])
      gaia_ids[gaia_id] = {"name":name}
      fallback_names[name] = {"gaia_id":gaia_id}
    return (gaia_ids,fallback_names)

class Message:
  def __init__():
    return

class TextContent:
  def __init__():
    return

class LinkContent:
  def __init__():
    return

class LinebreakContent:
  def __init__():
    return

class TextMessage:
  def __init__():
    return


def create_user_dict(hangouts, conversation_index):
  gaia_ids = {}
  fallback_names = {}
  participant_data = hangouts["conversation_state"][conversation_index]["conversation_state"]["conversation"]["participant_data"]
  for participant in participant_data:
    gaia_id = participant["id"]["gaia_id"]
    name = participant.get("fallback_name",participant["id"]["gaia_id"])
    gaia_ids[gaia_id] = {"name":name}
    fallback_names[name] = {"gaia_id":gaia_id}
  return (gaia_ids,fallback_names)

def filter_by_timestamp(events,start_time=0,end_time=sys.maxsize):
  return filter(lambda e: int(e["timestamp"]) > start_time, events)

def count_messages(hangouts, conversation_index, users):
  count = {}
  events = hangouts["conversation_state"][conversation_index]["conversation_state"]["event"]
#  print(len(events))
  events = filter_by_timestamp(events,1503906519000000)
#  print(len(events))
  #pprint(events)
  for event in events:
    gaia_id = event["sender_id"]["gaia_id"]
    if gaia_id not in count:
      count[gaia_id] = 1
    else:
      count[gaia_id] += 1
#    print users[gaia_id]["name"]
#    print event["chat_message"]["message_content"]["segment"][0]["text"]
#    print ""
  return count

# Translate the fallback_name to gaia_id
def _fallback_to_gaia(fallback_name, fallback_names):
  return  fallback_names[fallback_name]["gaia_id"]

def get_messages_for_user(hangouts, conversation_index, user):
  messages = []
  events = hangouts["conversation_state"][conversation_index]["conversation_state"]["event"]
  for event in events:
    if event["sender_id"]["gaia_id"] == user:
      messages.append(event)

def main():
  usage = "TODO"

  parser = argparse.ArgumentParser(description="Parse args", usage=usage)
  parser.add_argument("-f", "--dumpfile", required=True, help="Hangouts JSON file")
  parser.add_argument("-C", "--conversation_name", help="Conversation")
  parser.add_argument("-c", "--conversation_index", help="Conversation index")
  parser.add_argument("-u", "--user", help="Only one user")

  args = parser.parse_args()
  dumpfile = args.dumpfile
  conversation_index = args.conversation_index
  conversation_name = args.conversation_name
  user = args.user

  conversation_index = 18

  print(dumpfile)
  hangouts = Hangouts(filepath=dumpfile)
  #hangouts = Hangouts(filepath=dumpfile, conversation_name=conversation_name, conversation_index=conversation_index, user=user)

  gaia_ids, fallback_names = create_user_dict(hangouts, conversation_index)
#  print(json.dumps(gaia_ids, indent=2))
#  print(json.dumps(fallback_names, indent=2))

  #print _fallback_to_gaia(user, fallback_names)
  #sys.exit(0)

  '''
  count = count_messages(hangouts, conversation_index, gaia_ids)
  print(json.dumps(count, indent=2))
  for gaia_id, num in count.iteritems():
    print(gaia_id, num)
    print("{0}: {1}".format(gaia_ids[gaia_id]["name"], num))
  '''

if __name__ == "__main__":
  main()
