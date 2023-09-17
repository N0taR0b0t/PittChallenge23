#!/usr/bin/env python3.11

import os
import openai
import configparser

def check_substances_interactions(substance1, substance2):
    # Read secret data from the ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    apikey = config['openai']['apikey']

    model="gpt-3.5-turbo"
    openai.api_key = apikey
    inter = substance1 + " or " + substance2
    inter_message = ("Simply reply 'UNKNOWN' if either " + inter + " are not intended for human consumption. If both are designed to be ingested, provide a concise response, under 80 words, explaining problems that may arise if both are ingested together. Be formal, professional, cautious, and clear in the third person.")

    messages = [{
        "role": "system",
        "content": inter_message
    }]

    response = openai.ChatCompletion.create(model=model, messages=messages)

    #print("API Input:")
    #print(inter_message)
    #print("API Output:")
    print(response.choices[0].message['content'])

    return response.choices[0].message['content']

# Example of how to call the function
result = check_substances_interactions("grapefruit", "simvastatin")
