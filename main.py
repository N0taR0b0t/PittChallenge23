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

if __name__ == "__main__":

      ing = sys.argv[1]
      allergy = sys.argv[2]
      med = sys.argv[3]

    for i in range(len(ing)):
        if isAllergen(ing[i]):
            print(str(ing[i]) + "is an allergen")

        for m in range(len(med)):
            if hasDrugInteraction(ing[i]):
                print(str(ing[i]) + "has drug interaction with" + str(med[m]))
                # add chatGPT interaction + drugs.com




    except Error as e:
        print()
        print(("Error --" + e.msg))
        exit()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()




def isAllergen(food):
    # check food allergen list, retuns T/F
    return True
    return False

def hasDrugInteraction(food):
    # returns T/F

    return False
    return True
