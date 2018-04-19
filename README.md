# PyBot-Spark 
This is a Python 3 project built using Flask, for the creation of Cisco Spark Bots.

This project equips you with tools for creating Bots of any specification.

From a Bot that checks the weather, to one that monitors your Meraki estate; applications are endless.

## Overview

The emphasis of this project is to promote modularity and flexibility. It is designed to allow you to deliver functionality and utilize your own scripts quickly using Spark as an interface. This document provides a step by step guide to create a basic Cisco Spark Bot.

### Files

#### main.py

main.py is the core program of the project.

* Sets up flask instance and webhooks to allow connection between code & bot

* Deals with processing of requests (POST,GET)

* Logic to determine how the code responds to the request.

#### PyCiscoSpark.py

PyCiscoSpark.py is a library which contains GET,DELETE,POST,PUT Requests specified in the Cisco Spark API. This library is used in main.py to deal with requests used in the Spark API. 

# Bot Usage

## Prerequisites
Log into your Cisco Spark account. You'll need to start by adding your bot to the Cisco Spark website. https://developer.ciscospark.com/add-app.html


1.Click “create a bot”

2.Fill out all the details about your bot. 

3.Click "Add Bot", make sure to make a note of the “name”, “Bot Username” & “Bot’s Access Token”. You’ll need this in a second.


## ngrok - Skip this step if you already have an Internet reachable web-server

To connect the code to the bot a webhook needs to be made which requires a url. Ngrok is useful to quickly test this code however this will limit the bot to only work when your machine is up and running. Alternatively consider using a cloud based instance such as a Amazon EC2 which can be spun up quickly.

ngrok will make it easy for you to develop your code with a live bot. It will facilitate as an through put to allow the bot & code to communicate.
Please check: https://ngrok.com/download
After you've installed ngrok, in a terminal start the service:
    
`ngrok http 4000`
    
You should see a screen that looks like this (Take a note of the https address):
    
        ngrok by @inconshreveable                                                                                                                                 (Ctrl+C to quit)
        
        Session Status                online
        Version                       2.2.4
        Region                        United States (us)
        Web Interface                 http://127.0.0.1:4040
        Forwarding                    http://this.is.the.url.you.need -> localhost:4000
        Forwarding                    **https://this.is.the.url.you.need** -> localhost:4000 
        


## Install

Clone the project- 

Either by pressing "download" or "git clone https://scm.dimensiondata.com/ryan.byrne/PyBot_Spark"

Install the library requirements-

`pip install -r requirements.txt`

## Configure

In order to run, the service needs several pieces of information to be provided:

* Spark Account Email
* Spark Account name 
* Spark Bot Authentication Key to enable API Calls
* Spark Bot URL


In 'main.py' edit existing variables with your information- :

        if __name__ == "__main__":

        # Edit values for botEmail,botName,bot_url,accessToken
        # Access token can be generated using the CISCO BOT account
        botEmail = "yourBotIDHere>@sparkbot.io"  # bot's email address -change
        botName = "<BotNameHere>"
        bot_url = "<https://this.is.the.url.you.need/>"
        accessToken = "<PlaceAccessTokenHere>"  # Bot's access token
        port = 4000

Once this is complete, you are up and running and READY TO USE YOUR BOT!! :)

## Run

`python main.py`

....and say /hello to your Bot on Cisco Spark! 

# Accessing

Upon startup, the service registers a webhook to send all new messages to the service address.


## Interacting with the Spark Bot

The Spark Bot is a very simple interface that is designed to make it intuitive to use.  Simply send any message to the Spark Bot to have the bot reply back with some instructions on how to access the features.

The bot is deisgned to look for commands to act on, and provide the basic help message for anything else.  The following commands are already implemented to serve as examples:

* /date
  * The bot will reply with the date today
* /catFact
  * Returns a random cat fact
* /help 
  * Provides a help message -detailing all commands registered to the bot

## Adding new commands

Adding a new command to your bot is easy!

Steps:

* Open main.py

Commands are listed within the ‘commands’ array located in the main() of main.py to add a new command follow the following format:


` “<command>”: “<Description>” `

        commands = {
            "/help": "Get help.",
            "/hello": "Bot will say hello",
            "/date": "Returns the date for today", 
            "/newCommand": "This is a new command!"}

* In the function reply_for_messages() 
    * Find:
    
            if command in ["/help"]:
                reply = send_help()
            elif command in ["/hello"]:
                reply= "Hello I am a bot! please type /help to find out what I can do."
            elif command in ["/date"]:
                reply = "It is " + datetime.now().strftime('%A %d %B %Y') + " today."
            else:
                reply = "I cannot answer that - Here is what I can do: \n"
                reply= reply + send_help()

            Spark.post_message(accessToken, roomId,reply)

Follow the format adding a new Elif statement before the else statement: 

        elif command in ["/newCommand"]:
            reply= "This is a new command "
            
#### Note:

To implement additional functionality such as using an existing script to make API calls, make a call to the function/program and return a string. Pictures/files can be returned as well however the code will have to be modified using functionality from PySparkCisco.py to utilize that.


Thanks for reading! Hopefully you have a fully functioning Spark bot! If you have any questions/ideas/suggestions please let me know by raising an issue or email: ryanbyrne@dimensiondata.com
