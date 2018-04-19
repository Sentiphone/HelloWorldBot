from flask import Flask, request
import apiai
import requests
import json
from datetime import datetime
import PySparkCisco as Spark
app = Flask(__name__)

def get_cat():
    response = requests.get("https://catfact.ninja/fact", verify=False)
    json_data = response.json()
    cat_fact=json_data['fact']
    return cat_fact

def get_AI_output(text,ai):
    request = ai.text_request()
    request.query = text
    response = json.loads(request.getresponse().read().decode('utf-8'))
    message = response['result']['fulfillment']['speech']
    return message

def setup_webhook(at, name, targetUrl,resource,event):
    """ Sets up a specified webhook - will update webhook if it already exists otherwise will create a new webhook
        """
    webhooks=Spark.get_webhooks(at) #GET request for webhooks assigned to bot
    found_webhook=None
    print(webhooks)
    try:
        for i in webhooks['items']:
            if i['name'] == name:
                print("Found existing webhook. Updating it.\n")
                found_webhook=i
        if found_webhook is None:
            print("Creating new webhook")
            Spark.post_webhook(at,name,targetUrl,resource,event)
        else:
                webhook_id=found_webhook['id']
                Spark.put_webhook(at,webhook_id,name,targetUrl)
    except Exception as e:
        print("Encountered an error while updating webhook: {}".format(e))
    return



def send_help(toPersonEmail):
    """ Returns the welcome/help message
        -Initiated by adding the bot to a room or the user typing /help
    """
    message = "Hi <@personEmail:"+toPersonEmail+ ">\uD83D\uDC4B . I'm HelloWorldBot, Nice to meet you! \uD83D\uDEB2\uD83D\uDEB2\uD83D\uDEB2  \n \n"
    message = message+"Ask me a question and I'll answer it the best I can.  \n"
    message = message + "I also understand the following commands:  \n"
    for c in commands.items():
        message = message + "* `%s`: %s  \n" % (c[0], c[1])
    return message


@app.route('/', methods=['POST'])
def sort_tasks():
    """ Sorts POST requests initiated by events in Spark.
        Sorted into two groups: messages & memberships
    """
    resource_type=request.json.get('resource')
    print(resource_type)
    if resource_type=='messages':
        message_id = request.json.get('data').get('id')
        message_details= Spark.get_message(access_token,message_id)
        reply_for_messages(message_details)
    if resource_type=='memberships':
        add_person = request.json.get('data').get('personEmail')
        if add_person == bot_email:
            request_id=str(request.json.get('actorId'))
            person_detail=Spark.get_persondetails(access_token,request_id)
            request_email=str(person_detail['emails'][0])
            member_room=request.json.get('data').get('roomId')
            reply=send_help(request_email)
            Spark.post_message_markdown(access_token,member_room,reply)
    return ""

def reply_for_messages(response):
    """ Logic to determine how to respond to a message sent to the bot
        """
    print(response)
    command = ""
    input_message = response['text']
    person_email = response['personEmail']
    room_id=response['roomId']
    print(input_message)
    response_message = input_message.replace(bot_name, '').strip()
    print(response_message)

    if person_email == bot_email: #Prevents the bot from talking to itself
        return

    for c in commands.items():
        if response_message.find(c[0]) == 0:
            command = c[0]
            print("Found command: " + command + "\n")
            break

    if command in ["/help"]:
        reply = send_help(person_email)
    elif command in ["/catfact"]:
        reply=get_cat()
    elif command in ["/date"]:
        reply="it is " + datetime.now().strftime('%A %d %B %Y') + " today."
    else:
        reply = get_AI_output(response_message, ai)

    Spark.post_message_markdown(access_token,room_id,reply)
    return

if __name__ == "__main__":

    #Bot Credentials- Please modify the bot_url to a suitable url address that can be used for a webhook. E.g. Ngrok, Web server, Amazon EC2 instance.
    bot_email = "Proteus@sparkbot.io"  # bot's email address -change
    bot_name = "Proteus"
    bot_url = "https://064817eb.ngrok.io"
    access_token = "<Bot access token>"  # Bot access token
    api_ai = "<DialogFlow project access token> "  # access token for DialogFlow project
    ai = apiai.ApiAI(api_ai)
    port = 4000



    commands = {"/date": "Find out the date today", # Defined commands that the bot can recognize
        "/catfact": "A random cat fact!",
        "/help": "Get help."}

    setup_webhook(access_token,"MessageHook",bot_url,"messages","created")   #Sets a webhook to monitor message events
    setup_webhook(access_token, "MemberHook", bot_url,"memberships","created")  #Sets a webhook to monitor membership events
    print("Spark Bot URL (for webhook): " + bot_url )
    print("Spark Bot App Name: " + bot_email + "\n")
    app.run(host=("0.0.0.0"),port=port)


