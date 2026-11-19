from django.shortcuts import render, HttpResponse
import json

from .models import Item, Store

from django.db import connection

# Create your views here.
def home(request):
    # Request object taken as a parameter will allow us to access things like query parameters and the body of different requests that are
    # being sent to this function 
    # return HttpResponse("hello world!")

    return render(request, "home.html") # render the template, only works if templates are inside directory

def recipe_detail(request):
    with open('Recipes.json') as json_file:
        data = json.load(json_file)
    recipes = data['recipe']
    context = {"recipes": recipes}
    return render(request, "recipe.html", context)

def inventory_list(request):
    items = Item.objects.all().order_by('itemname')
    stores = Store.objects.all().order_by('storeid')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                i.itemID,
                it.itemName,
                i.storeID,
                s.address,
                i.quantity
            FROM Inventory AS i
            INNER JOIN Item AS it ON i.itemID = it.itemID
            INNER JOIN Store AS s ON i.storeID = s.storeID
            ORDER BY s.storeID, it.itemName
        """)

        columns = [col[0] for col in cursor.description]
        inventory_records = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    context = {
        'items': items,
        'stores': stores,
        'inventory_records': inventory_records,
    }

    return render(request, 'inventory.html', context)
