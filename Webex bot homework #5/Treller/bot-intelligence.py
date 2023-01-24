# Manages the bot in all its functionality, from reading the message sent by the client to processing the request, using the Trello API, and sending the response back to the client
from flask import Flask, request
import requests
import json
import config

############## Webex application ##############
webex_api_header = {"content-type": "application/json; charset=utf-8", "authorization": "Bearer " + config.webex_token}

############## Flask application ##############
app = Flask(__name__)

############## Trello application ##############
trello_api_url = 'https://api.trello.com/1/'
trello_api_header = {'content-type': 'application/json', 'accept': 'application/json'}

# Send message from bot to client (after a client sent a message)
@app.route("/", methods=["GET", "POST"])
def send_message():
	webhook = request.json
	url = 'https://webexapis.com/v1/messages'
	msg = {'roomId': webhook["data"]["roomId"]}
	sender = webhook["data"]["personEmail"]
	message = get_message().lower() # .lower() is only needed for case-insensitive string comparison (in this way commands are recognized regardless of upper or lower case letters)
	if (sender != config.bot_name):
		if (message == 'help' or message == 'start'):
			msg["markdown"] = 'Welcome to **Treller**! This bot allows you to easily interact with Trello.\nList of available commands:<ul><li>*Help* -> Bot information</li><li>*Cards in `<list>`* -> List the cards in the specified list</li><li>*New list `<list>`* -> Creates a new list</li><li>*New card `<card>` --- `<list>` --- `[desc]`* -> Creates a new card in the list with the description, if specified</li><li>*Secret* -> It will tell you a secret</li></ul>'
		elif (message.startswith('cards in ')):
                        cards = get_trello_cards(config.trello_board_id, message.removeprefix('cards in '))
                        if cards == None:
                                msg["markdown"] = 'No cards found'
                        else:
                                msg["markdown"] = str(len(cards)) + ' cards found:'
                                msg["markdown"] += '<ul>'
                                for card in cards:
                                        msg["markdown"] += '<li>' + card['name'] + '</li>'
                                msg["markdown"] += '</ul>'
		elif (message.startswith('new card ')):
                        message = message.removeprefix('new card ')
                        messages = message.split('---', 2) # 3 dashes are used to avoid confusing the card name or description with the command parameter separators

                        if len(messages) < 2:
                                msg["markdown"] = 'Invalid command format. Type **help** to see the correct usage.'
                        else:
                                card_name = messages[0].strip()
                                list_name = messages[1].strip()
                                description = None
                                if len(messages) > 2:
                                        description = messages[2].strip()

                                result = create_trello_card(config.trello_board_id, list_name, card_name, description)
                                if result == None:
                                        msg["markdown"] = 'The specified list does not exist! If you want to create one, use the command "**new list**".'
                                elif result == True:
                                        msg["markdown"] = 'Card successfully created!'
                                else:
                                        msg["markdown"] = 'Something went wrong during the creation. Try again later :('
		elif (message.startswith('new list ')):
                        list_name = message.removeprefix('new list ')
                        result = create_trello_list(config.trello_board_id, list_name)
                        
                        if result == None:
                                msg["markdown"] = 'The specified list already exists!'
                        elif result == True:
                                msg["markdown"] = 'List successfully created!'
                        else:
                                msg["markdown"] = 'Something went wrong during the creation. Try again later :('
		elif (message == 'secret'):
			msg["markdown"] = 'Did you really think it would be so easy to discover a secret? Type "super secret" in chat'
		elif (message == 'super secret'):
			msg["markdown"] = 'Really? Well maybe you really want to know this secret. Use the command "super super secret" :)'
		elif (message == 'super super secret'):
			msg["markdown"] = 'You can find the source code for this amazing bot [here](https://github.com/LorenzoServolini/IncuNov2022). But don\'t tell anyone!!'
		else:
			msg["markdown"] = 'Command not recognized. Type **help** to see the list of available commands!'
			
	response = requests.post(url, data=json.dumps(msg), headers=webex_api_header, verify=True)
	
	return response.text # Required by Flask to print/debug

# Get the message sent from the client
def get_message():
	webhook = request.json
	url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
	get_msgs = requests.get(url, headers=webex_api_header, verify=True)
	message = get_msgs.json()['text']
	return message

# Get all lists in a board
def get_trello_lists(board_id):
        get_lists_url = trello_api_url + 'boards/' + board_id + '/lists'
        data = {'key': config.trello_key, 'token': config.trello_token}
        
        reply = requests.get(get_lists_url, data=json.dumps(data), headers=trello_api_header)

        debug('Obtaining lists', reply.status_code)
        
        return reply.json()

# Get the id of a list in a board from its name
def get_trello_list_id(board_id, list_name):
        lists = get_trello_lists(board_id)

        for list in lists:
                if list['name'].lower() == list_name.lower(): # .lower() is needed to get the id regardless of upper and lower case
                        return list['id']
        return None

# Get cards in a list
def get_trello_cards(board_id, list_name):
        list_id = get_trello_list_id(board_id, list_name)
        if list_id == None:
                return None

        get_card_url = trello_api_url + 'lists/' + list_id + '/cards'
        data = {'key': config.trello_key, 'token': config.trello_token}

        reply = requests.get(get_card_url, data=json.dumps(data), headers=trello_api_header)

        debug('Obtaining cards', reply.status_code)
        
        return reply.json()

# Create a new card inside the specified list, in the specified board
def create_trello_card(board_id, list_name, card_name, card_description):
        list_id = get_trello_list_id(board_id, list_name)
        if list_id == None:
                return None # Specified list does not exist
        
        create_card_url = trello_api_url + 'cards'
        data = {'key': config.trello_key, 'token': config.trello_token, 'idList': list_id, 'name': card_name}
        if card_description != '' and card_description != None:
                data['desc'] = card_description

        reply = requests.post(create_card_url, data=json.dumps(data), headers=trello_api_header)

        debug('Create card', reply.status_code)
        
        return True if reply.status_code == 200 else False

# Create a new list inside the specified board (if it doesn't already exist)
def create_trello_list(board_id, list_name):
        list_id = get_trello_list_id(board_id, list_name)
        if list_id != None:
                return None # Specified list already exists
        
        create_card_url = trello_api_url + 'boards/'+ board_id + '/lists'
        data = {'key': config.trello_key, 'token': config.trello_token, 'name': list_name}

        reply = requests.post(create_card_url, data=json.dumps(data), headers=trello_api_header)

        debug('Create list', reply.status_code)
        
        return True if reply.status_code == 200 else False


# Print (on terminal) a message based on the status of the API server response
def debug(action, status_code):
        if status_code == 200:
            print (action + ' completed with success')
        else:
            print ('Something wrong happened: ' + reply.status_code)


app.run(debug = True)
