from abc import ABC, abstractmethod

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
    def change(self, Menu):
        """Changes item in menu list."""
        pass





    @abstractmethod
    def display(self, Menu):
        """Displays menu item's name, price"""
        import json
        import pandas as pd


