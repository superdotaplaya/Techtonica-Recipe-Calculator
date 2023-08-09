from audioop import avg
import os, sys, discord, platform, random, aiohttp, json
from datetime import datetime
import time
import json

import requests
import threading
import asyncio

recipes_list = []
task = ""


def define_task():
    task = input("Welcome to my Techtonica recipe lookup tool and calculator, please enter 'calculate' to figure out toal number of items needed to bulk craft, or enter 'lookup' to lookup the recipe of one item: ")



    if task.lower() == "calculate":
        task = "calculate"
        user_request_lookup(task)
    if task.lower() == "lookup":
        task = "lookup"
        user_request_lookup(task)
    else:
        define_task()

# Asks rthe user for the name of the item they are looking for
def user_request_lookup(task):
    requested_item = input("What item are you looking for the recipe of?")
    find_recipe(requested_item, task)


#Seqarches for the requested item in the CSV file.
def find_recipe(requested_item, task):
    found = False
    for item in recipes_list:

        #if the user is looking up the recipe for 1 item, just finds the recipe
        if item[0].title() == requested_item and task == "lookup":
            item_recipe = " \n ".join(item[1:-1])
            print(f"Recipe for {requested_item} is: {item_recipe}")
            found = True
            requested_item = input("If you would like to find the recipe of another item, please enter it now: ")
            find_recipe(requested_item)

        # if the user is looking to calculate multiple of the same item, calculate the total needed of each component to craft the requested item

        if item[0].title() == requested_item and task == "calculate":
            components = []
            total_amounts = []
            amounts = []
            #Ignores the final item component because in the csv, the final item is always a linebreak (\n)
            for item in item[1:-1]:
                component = []

                #breakup each line of csv into seperate words for further processing
                component.append(item.split(" "))

                #combine multiword components together to be listed as one component
                amounts.append("".join(filter(str.isdigit, item)))
                found = True

                #add this component name to the components list
                components.append(component[0][1:])

                #figure out how many the user is trying to craft
            requested_amount = input("How many of these are you trying to create? ")
            
            #perform needed calculations to get totals needed for each item
            for item in amounts:
                total_amount = int(item) * int(requested_amount)
                total_amounts.append(total_amount)
             
            final_components_list = []
            i=0

            #Construct the final string with all components and amounts listed in one string for easier reading by the user.
            for item in total_amounts:
                final_components_list.append(str(item) +" " + " ".join(components[i]))
                i+=1

            return(f"To craft {requested_amount} {requested_item}(s), you need the following totals: {', '.join(final_components_list)}")





    if found == False and task.lower() == "lookup":
        print("Sorry, we were unable to find the item you are looking for :( Check the spelling, or try a different item)")
        user_request_lookup()
    elif found == False and task.lower() == "calculate":
        print("cant find it")



#open and read the csv file for use as a database of game recipes
requested_item = ""
raw_data_file = open("Recipes.csv","r+")
raw_data_lines = raw_data_file.readlines()
for line in raw_data_lines:
    recipe = line.split(",")
    recipes_list.append(recipe)


#run the main loop
define_task()







