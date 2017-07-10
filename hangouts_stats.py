#!/usr/bin/python

import sys

import json
import pprint
from optparse import OptionParser

def load_hangouts(dumpfile):
  with open(dumpfile) as data_file:
      return json.load(data_file)

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

def count_messages(hangouts, conversation_index, users):
  count = {}
  events = hangouts["conversation_state"][conversation_index]["conversation_state"]["event"]
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

  parser = OptionParser(usage=usage)
  parser.add_option("-f", "--dumpfile", help="Hangouts JSON file")
  parser.add_option("-C", "--conversation_name", help="Conversation")
  parser.add_option("-c", "--conversation_index", help="Conversation index")
  parser.add_option("-u", "--user", help="Only one user")

  (options, args) = parser.parse_args()
  dumpfile = options.dumpfile
  conversation_index = options.conversation_index
  conversation_name = options.conversation_name
  user = options.user

  conversation_index = 17

  if dumpfile is None:
    print("Error, no dumpfile specified with -f/--file")
    parser.print_help()
    return

  hangouts = load_hangouts(dumpfile)
  gaia_ids, fallback_names = create_user_dict(hangouts, conversation_index)
  print(json.dumps(gaia_ids, indent=2))

  #print _fallback_to_gaia(user, fallback_names)
  #sys.exit(0)

  count = count_messages(hangouts, conversation_index, gaia_ids)
  for gaia_id, num in count.iteritems():
    print "{0}: {1}".format(gaia_ids[gaia_id]["name"], num)

if __name__ == "__main__":
  main()
