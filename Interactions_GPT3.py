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
    inter = substance1 + " and " + substance2
    inter_message = ("Provide a concise response under 100 words, explaining what problems, if any, that may arise if both " + inter + " are ingested together. Be formal, professional, cautious, and clear in the third person. Include some technical details to explain the underlying mechanisms.")

    messages = [{
        "role": "system",
        "content": inter_message
    }]

    response = openai.ChatCompletion.create(model=model, messages=messages)

    #print("API Output:")
    #print(response.choices[0].message['content'])
    return response.choices[0].message['content']

# Example of how to call the function
result = check_substances_interactions("grapefruit", "simvastatin")
print(result)
