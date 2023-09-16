#!/usr/bin/env python3.11
# encoding: utf-8

"""
Ingredients handler for Pitt Challange Hackathon
Created September 15th, 2023
Updated September 15th, 2023
Version: 0.0

Takes list arguments ingedients, allergies, medication
"""

import json, os, sys, subprocess


def isAllergen(food):
    # check food allergen list, retuns T/F
    with open('allergens.txt') as in_file:
        for line in in_file:
            line = line.strip()
            if line == food:
                return True
        return False

def hasDrugInteraction(food):
    # returns T/F

    return False
    return True

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
            print(str(ing[i]) + " is a first generation antihystamine")
        if ing[i] in ["IBUPROPHEN", "ASPRIN", "NAPROXEN"]:
            print(str(ing[i]) + " is an NSAID")
        if ing[i] in ["ALCOHOL", "ETHANOL"]: # which are we using?
            print("This product contains alcohol")
        if ing[i] in ["CAFFEINE"]:
            print("This product contains caffeine")
        if ing[i] in ["MILK", "LACTOSE", "WHEY", "CURDS"[: # not comprehensive]
            print("This product contains lactose")


        if isAllergen(ing[i]):
            print(str(ing[i]) + " is an allergen")

        for m in range(len(med)):
            if hasDrugInteraction(ing[i]):
                print(str(ing[i]) + "has drug interaction with" + str(med[m]))
                # add chatGPT interaction + drugs.com

