from abc import ABC, abstractmethod
import json
import pandas as pd

class MenuInterface(ABC):
    @abstractmethod
    def add(self, Menu):
        """Adds item to menu list."""
        pass





    @abstractmethod
    def remove(self, Menu):
        """Removes item from menu list."""
        pass






    @abstractmethod
    def change(self, temp, p, u ):
        """Changes item in menu list."""
        import json
        fd = open("Recipes.json","r") # Open file in read mode
        txt = fd.read() # reading data from file
        data = json.loads(txt)
        fd.close

        for recipe in data["recipe"]:
            if recipe["id"] == temp:
                if p in recipe.keys():
                    recipe[p] = u
                    print("Product ID " + str(temp) + "'s attriubute " + str(p) + "is Updated Successfully")
                else: 
                     print("Invalid Productattribute")
                break
        else:
            print("Invalid Product ID")

        js = json.dumps(data)
        fd = open("Recipes.json","w") # Open file in write mode
        fd.write(js) # writing data to file
        fd.close()






    @abstractmethod
    def display(self, Menu):
        """Displays menu item's name, price"""
        fd = open("Recipes.json","r") # Open file in read mode
        txt = fd.read() # reading data from file
        data = json.loads(txt)

        # Parse JSON data and populate a Python dictionary with the data
        





class Test(MenuInterface):
    def add(self, Menu): pass
    def remove(self, Menu): pass
    def display(self, Menu): pass
    def change(self, temp, p, u):
        super().change(temp, p, u)

Test().change("R101", "price", 24.99)