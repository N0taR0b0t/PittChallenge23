#!/usr/bin/env python3.11
# encoding: utf-8

"""
Ingredients handler for Pitt Challange Hackathon
Created September 15th, 2023
Updated September 17th, 2023
Version: 0.4

Takes list arguments ingedients, allergies, medication
"""

import json, os, sys, subprocess, csv, requests, magic
import pprint
import urllib.parse
import OCR
import category
#import DrugNames
from medInteractGPT import check_substances_interactions


def isAllergen(food):
    # check food allergen list, retuns T/F
#    with open('allergens.txt') as in_file:
#        for line in in_file:
#            line = line.strip()
#            if line == food:
#                return True
#        return False
    with open('COMPARE.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in enumerate(spamreader):
            if row[1][1].strip().upper() == food:
                for i in allergy:
                    if row[1][3] == i:
                        return True

def to_upper(oldList):
    newList = []
    for element in oldList:
        newList.append(element.upper())
    return newList

def hasDrugInteractionNIH(foodwithRX, medlist):
    # returns T/F
    uri = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"
    if foodwithRX == '':
        params = {'format': '.json', 'rxcuis': medlist} # yes interacts
    else:
        params = {'format': '.json', 'rxcuis': foodwithRX + medlist} # yes interacts

    # Create a dictionary with the request parameters
    #params = {'format': '.json', 'rxcuis': [12255944,7739116,6365314,6364742,12251372]}
#    params = {'format': '.json', 'rxcuis': [6397347,10298100],'sources':"DrugBank"}
    try:
        r = requests.get(uri, params)
        r.raise_for_status()  # Raise an exception for HTTP errors
        if r.status_code != 200:
            print("Response Status Code:", r.status_code)
#        pprint.pprint(r.json())
        # You can return True/False based on the API response here
        # if there is a drug interaction return true else return false
#        delete
        jNIH = r.json()
        removeList = ['nlmDisclaimer', 'sourceDisclaimer']
        for i in range(len(removeList)):
            if removeList[i] in jNIH:
                del jNIH[removeList[i]]
        if jNIH == {}:
            return False
        return jNIH
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        # Handle the error or return False
        return False

# Call the function with a sample 'food' value
#hasDrugInteraction("sample_food")


def get_rxnorm_code(medication_name):
    # Base URL for the RxNav API
    base_url = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
    # Parameters for the API request
    params = {
        "name": medication_name
    }

    try:
        # Make the GET request to the RxNav API
        response = requests.get(base_url, params=params)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Check if a match was found
            if "idGroup" in data:
                rxcui = data["idGroup"]["rxnormId"][0]
                return rxcui
            else:
                return False # NOT FOUND
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return False
#        return f"An error occurred: {str(e)}"

def hasDrugInteractionDB(food): # dep due to lack of API key
    uri = "https://api.drugbank.com/v1/ddi?"
    # Create a dictionary with the request parameters
#    params = {'ndc': "0054-0020,0456-2005"}
    params = {'q': "lithium,lexapro", "Authorization": ""} # need API key

    try:
        r = requests.get(uri, params)
        r.raise_for_status()  # Raise an exception for HTTP errors
        if r.status_code != 200:
            print("Response Status Code:", r.status_code)
        pprint.pprint(r.json())
        # You can return True/False based on the API response here
        # if there is a drug interaction return true else return false
    except requests.exceptions.RequestException as e:
        print("Request Exception:", e)
        # Handle the error or return False

# Call the function with a sample 'food' value
#hasDrugInteractionDB("sample_food")


#def descriptions(data):
    #for group in data['fullInteractionTypeGroup']:
    #    for entry in group['fullInteractionType']:
    #        for interaction in entry['interactionPair']:
    #            return interaction['description']

def descriptions(data):
    descriptions = []
    for group in data['fullInteractionTypeGroup']:
        for entry in group['fullInteractionType']:
            for interaction in entry['interactionPair']:
                descriptions.append(interaction['description'])
    return '\n'.join(descriptions)

def get_names_with_interaction_pairs(data):
    names_with_pairs = set()
    for group in data['fullInteractionTypeGroup']:
        for entry in group['fullInteractionType']:
            min_concepts = entry['minConcept']
            if min_concepts:
                for min_concept in min_concepts:
                    names_with_pairs.add(min_concept['name'])
    return names_with_pairs


# Extract medication names for each interaction pair
medication_pairs = []

def get_pairs(data):
    for group in data['fullInteractionTypeGroup']:
        for interaction_type in group['fullInteractionType']:
            for interaction_pair in interaction_type['interactionPair']:
                concept1 = interaction_pair['interactionConcept'][0]['minConceptItem']['name']
                concept2 = interaction_pair['interactionConcept'][1]['minConceptItem']['name']
                medication_pairs.append((concept1, concept2))

    return medication_pairs

#with open(sys.argv[1]) as in_file:
#ing = sys.argv[1].split("\n")

firstparam = sys.argv[1]
secondparam = sys.argv[2]
thirdparam = sys.argv[3]

#print(os.path.exists(sys.argv[1]))
if os.path.isfile(firstparam) == True:
    if magic.from_file(firstparam, mime=True).startswith("image"):
        ing = OCR.get_image_ingredients(firstparam)
        print(ing)
    else:
        ing = []
        with open(firstparam) as in_file:
            for line in in_file:
                   line = line.strip()
                   ing.append(line)
else:
    ing = []
    ing = to_upper(firstparam.split(","))

print(ing)

allergy = []
if os.path.isfile(secondparam) == True:
    with open(secondparam) as in_file:
            for line in in_file:
                line = line.strip()
                allergy.append(line)
else:
    allergy = to_upper(secondparam.split(","))



med = []
if os.path.exists(sys.argv[3]):
    with open(sys.argv[3]) as in_file:
        for line in in_file:
            line = line.strip()
            if line.isdigit():
                med.append(int(line))
            else:
                med.append(get_rxnorm_code(line))
else:
    med = to_upper(sys.argv[3].split(","))
    for i in range(len(med)):
        if not med[i].isdigit():
            med[i] = get_rxnorm_code(med[i])

# clear whitespace --- other sanitization
#simpIng = []
#stripping = []
#for i in range(len(ing)):
#    stripping.append(ing[i].strip())
#    if str(category.search_substance(ing[i],1)) == "None":
#        simpIng.append(ing[i])
#    else:
#        simpIng.append(category.search_substance(ing[i],1))

#ing = stripping

for i in range(len(allergy)):
    allergy[i] = allergy[i].strip()
for i in range(len(med)):
    med[i] = med[i].strip()



foodmedRX = []
for i in ing:
    code = get_rxnorm_code(i)
    if code != False:
        foodmedRX.append(code)
#    print("No such file '{}'".format(sys.argv[3]), file=sys.stderr)
#    med = ""

if __name__ == "__main__":
#    ing = sys.argv[1]
    print("Complete list of ingredients passed: " + str(ing))
    print("Genericicized list of ingredients passed: " + str(simpIng))
#    allergy = sys.argv[2]
#    med = list(sys.argv[3]) # less than 4 (4+1=5 API limit)
    print("There are " + str(len(med) + len(foodmedRX)) + " drugs or medically active ingredients")

#    print(foodmedRX)
#    print(med)
    if len(foodmedRX) + len(med) <= 5: # we are API limited to 5 interactions at a time being checked. Could check each permutation 
        nihResp = hasDrugInteractionNIH(foodmedRX,med)  # more going on biologically means it's harder to know if an interaction will happen: more chaos (gene, env)
    else:
        print("Cannot Process Request: too many medicinal ingredients (>5)")
        print("Running missing some food-drug interactions")
        items = int(5 - len(med))
        if items <= 0:
            print("Running missing some drug-drug interactions")
            nihResp = hasDrugInteractionNIH('',med[0:4])
        else:
            nihResp = hasDrugInteractionNIH(foodmedRX[0:items],med[0:len(med)])

    print()

    if nihResp != False:
#            print(nihResp)
#            interaction_pairs = nihResp['fullInteractionTypeGroup'][0]['fullInteractionType'][0]['interactionPair']
#            print(interaction_pairs)
#            descriptions = [pair['description'] for pair in interaction_pairs]
#            names = [  (pair['interactionConcept'][0]['minConceptItem']['name'], pair['interactionConcept'][1]['minConceptItem']['name'])
#                 for pair in interaction_pairs    ][0]
        print(descriptions(nihResp))
#        print(get_names_with_interaction_pairs(nihResp))
        pairs = get_pairs(nihResp)
        print()
        for x in pairs:
            print(x[0],x[1])
            print(check_substances_interactions(x[0],x[1])) ###########333

    print()
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
            print("You are allergic to " + ing[i])

#        for m in range(len(med)):
#            if hasDrugInteraction(ing[i],med): # depricated
#                print(str(ing[i]) + "has drug interaction with" + str(med[m]))
                # add chatGPT interaction + drugs.com



    print()
    print("Done!")
