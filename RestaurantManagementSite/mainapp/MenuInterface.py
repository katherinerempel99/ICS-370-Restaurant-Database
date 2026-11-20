from abc import ABC, abstractmethod
import json
import pandas as pd

class MenuInterface(ABC):
    @abstractmethod
    def add(self, Menu):
        """Adds item to menu list."""
        pass





    @abstractmethod
    def remove(self, recipeID):
        """Removes a recipe from the JSON menu."""
        from .MenuRemove import remove_recipe
        return remove_recipe(recipeID)






    @abstractmethod
    def change(self, Menu):
        """Changes item in menu list."""
        pass





    @abstractmethod
    def display(recipeID):
        """Displays menu item's name, price"""
        fd = open("Recipes.json","r") # Open file in read mode
        txt = fd.read() # reading data from file
        data = json.loads(txt)
        fd.close()
        
        # Following code will filter out recipeID from records
        if recipeID in data.keys():
            temp = pd.DataFrame(columns=["id"])
            temp["id"] = [i]

            for j in data[i].keys():
                temp[j] = data[i][j]

            from IPython.display import display
            display(temp)
            
        else:
            print("You have entered wrong product ID that is not present in database!")
   # display("R101")



