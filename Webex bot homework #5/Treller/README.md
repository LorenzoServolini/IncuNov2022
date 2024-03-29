0. Install libraries:
	- `pip install requests`
	- `pip install Flask`
1. Create a new bot from https://developer.webex.com/my-apps
2. Move configuration `ngrok.yml` inside `%USERPROFILE%\.ngrok2\` (this will set the region of ngrok)
3. Set all the necessary data (API tokens, bot name...) in the `config.py` file
4. Download [ngrok](https://ngrok.com/download), move it to the `../ngrok` folder and run it with `Run ngrok.bat`
5. Setup the webhook:
	- Copy `"Forwarding"` address in `"targetUrl"` at https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook <br/>
	(If you paste that address into your browser you will have information about the requests that come through ngrok)
	- Insert token in the `"Authorization"` field <br/>
	- Insert `messages` in the `"resource"` field <br/>
	- Insert `created` in the `"event"` field <br/>
	- Insert a name you like in the `"name"` field and click the `"Run"` button <br/>
	(If this is not the first time you do this, delete previous Webhooks; otherwise multiple requests are sent for each message sent)
6. Run bot with `Run bot.bat`
7. When you want to turn off the bot, Ctrl+C on both shells (Python program and ngrok)

<br/>

Webex API:
- Useful webhook links: <br/>
	https://developer.webex.com/docs/api/v1/webhooks <br/>
	https://developer.webex.com/docs/api/v1/webhooks/list-webhooks <br/>
	https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook <br/>
	https://developer.webex.com/docs/api/v1/webhooks/delete-a-webhook <br/>
- Useful message links: <br/>
	https://developer.webex.com/docs/api/v1/messages/list-messages

Trello:
- Useful API links: <br/>
	https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/ <br/>
	https://www.postman.com/
