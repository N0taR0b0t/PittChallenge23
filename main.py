#!/usr/bin/env python3.11
# encoding: utf-8

"""
Ingredients handler for Pitt Challange Hackathon
Created September 15th, 2023
Updated September 15th, 2023
Version: 0.0

Takes list arguments ingedients, allergies, medication
"""

import json, os, sys, subprocess, csv, requests
import pprint
import urllib.parse


def isAllergen(food):
    # check food allergen list, retuns T/F
    with open('allergens.txt') as in_file:
        for line in in_file:
            line = line.strip()
            if line == food:
                return True
        return False

def hasDrugInteractionNIH(food):
    # returns T/F
    uri = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
    # Create a dictionary with the request parameters
#    params = {'format': '.json', 'rxcuis': [152923,656659],'sources':"DrugBank"} # yes interacts
    #params = {'format': '.json', 'rxcuis': [12255944,7739116,6365314,6364742,12251372]}
#    params = {'format': '.json', 'rxcuis': [6397347,10298100],'sources':"DrugBank"}
    try:
        r = requests.get(uri, params)
        r.raise_for_status()  # Raise an exception for HTTP errors
        print("Response Status Code:", r.status_code)
        pprint.pprint(r.json())
        # You can return True/False based on the API response here
        # if there is a drug interaction return true else return false
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        # Handle the error or return False

# Call the function with a sample 'food' value
#hasDrugInteraction("sample_food")


def hasDrugInteractionDB(food):
    uri = "https://api.drugbank.com/v1/ddi?"
    # Create a dictionary with the request parameters
#    params = {'ndc': "0054-0020,0456-2005"}
    params = {'q': "lithium,lexapro", "Authorization": } # need API key

    try:
        r = requests.get(uri, params)
        r.raise_for_status()  # Raise an exception for HTTP errors
        print("Response Status Code:", r.status_code)
        pprint.pprint(r.json())
        # You can return True/False based on the API response here
        # if there is a drug interaction return true else return false
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        # Handle the error or return False

# Call the function with a sample 'food' value
hasDrugInteractionDB("sample_food")




ing = []

with open(sys.argv[1]) as in_file:
        for line in in_file:
            line = line.strip()
            ing.append(line)

if __name__ == "__main__":
#    ing = sys.argv[1]
    print(ing)
    allergy = sys.argv[2]
    med = sys.argv[3]

    for i in range(len(ing)):

        # Check for notable ingredients
        if ing[i] in ["DIPHENHYDRAMINE","DIMENHYDRINATE","CHLORPHENIRAMINE","DOXYLAMINE"]:
            print(str(ing[i]) + " is a first generation antihistamine")
        if ing[i] in ["IBUPROPHEN", "ASPRIN", "NAPROXEN"]:
            print(str(ing[i]) + " is an NSAID")
        if ing[i] in ["ALCOHOL", "ETHANOL"]: # which are we using?
            print("This product contains alcohol")
        if ing[i] in ["CAFFEINE"]:
            print("This product contains caffeine")
        if ing[i] in ["MILK", "LACTOSE", "WHEY", "CURDS"]: # not comprehensive
            print("This product contains lactose")


        if isAllergen(ing[i]):
            print(str(ing[i]) + " is an allergen")

        for m in range(len(med)):
            if hasDrugInteraction(ing[i]): # depricated
                print(str(ing[i]) + "has drug interaction with" + str(med[m]))
                # add chatGPT interaction + drugs.com

