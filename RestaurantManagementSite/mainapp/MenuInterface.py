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
        """Removes a menu item from the database."""
        from .MenuRemove import remove_menu
        return remove_menu(Menu)






    @abstractmethod
    def change(self, Menu):
        """Changes item in menu list."""
        pass





    @abstractmethod
    def display(self, Menu):
        """Displays menu item's name, price"""
        fd = open("Recipes.json","r") # Open file in read mode
        txt = fd.read() # reading data from file
        data = json.loads(txt)

        # Parse JSON data and populate a Python dictionary with the data
        


