from abc import ABC, abstractmethod
import json
import pandas as pd

class MenuInterface(ABC):
    @abstractmethod
    def add(self, Menu):
        pass

    @abstractmethod
    def remove(self, recipeID):
        pass

class RestaurantMenu(MenuInterface):
    def add(self, Menu):
        fd = open("Recipes.json", 'r')
        txt = fd.read()
        data = json.loads(txt)
        fd.close()

        print("Enter New Product ID :- ")
        product_id = input()

        if product_id not in data.keys():
            print("Enter Product Name :- ")
            name = input()
            
            print("Enter Price of Product :- ")
            price = input()
            
            print("Enter Category of Product :- ")
            category = input()
            
            print("Enter Quantity of Product :- ")
            quantity = input()
            
            print("Enter The Date on Which Product is Added in Inventory :- ")
            date = input()
            
            data[product_id] = {
                'name': name, 
                'price': price,
                'category': category, 
                'quantity': quantity, 
                'date': date
            }
            
            print("Please Press '0' to Add New Attributes or Press '1' to Continue :- ")
            z = int(input())
            
            if(z == 0):
                print("Enter Number of New Attributes/Properties of Product :- ")
                n = int(input())
                
                for i in range(n):
                    print("Enter Attribute Name That you Want To Add :- ")
                    nam = input()
                    print("Enter The " + str(nam) + " of Product :- ")
                    pro = input()
                    data[product_id][nam] = pro
                    
            print("Product ID " + str(product_id) + " Added Successfully...!!!")
            
            js = json.dumps(data, indent=4)
            fd = open("Recipes.json", 'w') 
            fd.write(js)
            fd.close()
            
        else:
            print("The Product ID you Have Entered Is Already Present in DataBase Please Check...!!!")

    def remove(self, recipeID):
        """Removes a recipe from the JSON menu."""
        from .MenuRemove import remove_recipe
        return remove_recipe(recipeID)

if __name__ == "__main__":
    # Call the function
    my_menu = RestaurantMenu()
    my_menu.add(None)







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
                    print("Product ID " + str(temp) + "'s attribute " + str(p) + "is Updated Successfully")
                else: 
                    print("Invalid Product attribute")
                break
        else:
            print("Invalid Product ID")

        js = json.dumps(data)
        fd = open("Recipes.json","w") # Open file in write mode
        fd.write(js) # writing data to file
        fd.close()






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






class Test(MenuInterface):
    def add(self, Menu): pass
    def remove(self, Menu): pass
    def display(self, Menu): pass
    def change(self, temp, p, u):
        super().change(temp, p, u)

# Test().change("R101", "price", 24.99)
