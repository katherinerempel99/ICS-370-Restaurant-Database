# Import JSON module
import json


# Open JSON file
with open('Recipes.json') as json_file:
    data = json.load(json_file) # turns json into a dictionary with recipe as the top level key

    # Print the type of data variable
    # print("Type:", type(data))

    # Print the data of dictionary in key-value pairs
    # print("\nRecipe:", data['recipe'])
    print("\nPrinting nested dictionary as a key-value pair\n") 
    for i in data['recipe']:
        print("Name:",i['name']) # returns names of recipes

def addRecipe():
    # have a fillable form that appends itself to Recipes.json
    return print("Recipe added.")

def removeRecipe():
    # perhaps a button next to the recipe that only owners can see?
    return print("Recipe removed.")